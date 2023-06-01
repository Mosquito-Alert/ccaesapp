from django.shortcuts import render
from django.utils import timezone
import datetime as dt
from datetime import date, timedelta
from django.db import connection
from main.models import ParticipationData, ObservationData, ObservationBarChartData, DataUpdateMetadata, SpeedMeterData, RuntimeSettings
from django.contrib.auth.decorators import login_required, user_passes_test
import json


def get_ccaa_name_from_code(code):
    cursor = connection.cursor()
    cursor.execute("""
        select name_latn from nuts_europe where nuts_id = %s
    """,(code,))
    result = cursor.fetchone()
    return result[0]


def get_tabular_data(ccaa_code,year):
    data = [[d.provincia, d.municipi, d.n_albo, d.trampeo_albo, d.ma_albo, d.n_culex, d.n_bite ] for d in ObservationData.objects.filter(ccaa_code=ccaa_code).filter(year=year) ]
    return data


def get_participation_data(year):
    total_participation_mosquitos = [[d.ccaa_name, d.n] for d in ParticipationData.objects.filter(category='mosquito').filter(year=year).order_by('-n') ]
    total_participation_sites = [[d.ccaa_name, d.n] for d in ParticipationData.objects.filter(category='site').filter(year=year).order_by('-n')]
    total_participation_bites = [[d.ccaa_name, d.n] for d in ParticipationData.objects.filter(category='bite').filter(year=year).order_by('-n')]
    return {'mosquito': total_participation_mosquitos, 'bite': total_participation_bites, 'site': total_participation_sites}


def get_speedmeter_data(ccaa=None):
    current_date = timezone.now()
    date_7_days_ago = current_date - timedelta(days=7)
    if ccaa is None:
        reports_last_seven = SpeedMeterData.objects.filter(creation_time__gte=date_7_days_ago).filter(creation_time__lte=current_date)
    else:
        reports_last_seven = SpeedMeterData.objects.filter(nuts_2=ccaa).filter(creation_time__gte=date_7_days_ago).filter(creation_time__lte=current_date)

    date_intervals = []
    days = 7
    while days >= 0:
        date_intervals.append(current_date - timedelta(days=days))
        days -= 1

    results = []
    for idx, val in enumerate(date_intervals):
        if idx + 1 >= len(date_intervals):
            break
        if ccaa is None:
            r = SpeedMeterData.objects.filter(creation_time__gte=date_intervals[idx]).filter(creation_time__lte=date_intervals[idx + 1])
        else:
            r = SpeedMeterData.objects.filter(nuts_2=ccaa).filter(creation_time__gte=date_intervals[idx]).filter(creation_time__lte=date_intervals[idx + 1])
        results.append(len(r))

    total = 0
    for result in results:
        total = total + result
    avg = total / len(results)

    data = {'reports_last_seven': len(reports_last_seven), 'avg_last_seven': avg}
    return data


@login_required
@user_passes_test(lambda u: u.is_superuser)
def index_par(request, ccaa=None, year=None):
    ccaa_name = get_ccaa_name_from_code(ccaa)
    ccaa_code = ccaa
    year_name = year


    dataSet = get_tabular_data(ccaa_code, year_name)
    participation_data = get_participation_data(year_name)

    update_barchart = DataUpdateMetadata.objects.get(class_name=ObservationBarChartData._meta.verbose_name)
    update_observations = DataUpdateMetadata.objects.get(class_name=ObservationData._meta.verbose_name)
    update_participation = DataUpdateMetadata.objects.get(class_name=ParticipationData._meta.verbose_name)
    update_gauges = DataUpdateMetadata.objects.get(class_name=SpeedMeterData._meta.verbose_name)

    all_sliced = [ [ d.n, d.month,d.category ] for d in ObservationBarChartData.objects.filter(ccaa_code=ccaa).filter(year=year)]

    no_data_barchart = True
    if len(all_sliced) == 0:
        no_data_barchart = False

    is_tabular_data_present = tabular_data_present(participation_data)

    context = {
        'all_sliced': json.dumps(all_sliced),
        'no_data_barchart': no_data_barchart,
        'ccaa_name': ccaa_name,
        'year_name': year_name,
        'dataSet': json.dumps(dataSet),
        'tabular_data_present': is_tabular_data_present,
        'participation_data': json.dumps(participation_data),
        'update_barchart': update_barchart,
        'update_observations': update_observations,
        'update_participation': update_participation,
        'update_gauges': update_gauges,
    }

    return render(request, 'main/index.html', context)


def tabular_data_present(participation_data):
    for p in participation_data:
        if p[2] != 0 or p[3] != 0 or p[4] != 0 or p[5] != 0:
            return True
    return False

# Create your views here.
@login_required
def index(request):
    this_user = request.user

    nuts = this_user.profile.nuts
    if nuts is None:
        ccaa_name = "Cataluña"
        ccaa_code = 'ES51'
    else:
        ccaa_name = get_ccaa_name_from_code(nuts.nuts_id)
        ccaa_code = nuts.nuts_id

    try:
        r = RuntimeSettings.objects.get(name='default_year')
        year_name = int(r.value)
    except RuntimeSettings.DoesNotExist:
        year_name = 2023

    dataSet = get_tabular_data(ccaa_code, year_name)
    participation_data = get_participation_data(year_name)
    all_sliced = [ [ d.n, d.month,d.category ] for d in ObservationBarChartData.objects.filter(ccaa_code=ccaa_code).filter(year=year_name)]

    update_barchart = DataUpdateMetadata.objects.get(class_name=ObservationBarChartData._meta.verbose_name)
    update_observations = DataUpdateMetadata.objects.get(class_name=ObservationData._meta.verbose_name)
    update_participation = DataUpdateMetadata.objects.get(class_name=ParticipationData._meta.verbose_name)
    update_gauges = DataUpdateMetadata.objects.get(class_name=SpeedMeterData._meta.verbose_name)

    no_data_barchart = True
    if len(all_sliced) == 0:
        no_data_barchart = False

    is_tabular_data_present = tabular_data_present(participation_data)

    speedmeter_data_ccaa = get_speedmeter_data(ccaa_code)
    speedmeter_data_global = get_speedmeter_data()

    context = {
        'all_sliced': json.dumps(all_sliced),
        'no_data_barchart': no_data_barchart,
        'ccaa_name': ccaa_name,
        'year_name': year_name,
        'dataSet': json.dumps(dataSet),
        'tabular_data_present': is_tabular_data_present,
        'participation_data': json.dumps(participation_data),
        'update_barchart': update_barchart,
        'update_observations': update_observations,
        'update_participation': update_participation,
        'update_gauges': update_gauges,
        'speedmeter_data_ccaa': speedmeter_data_ccaa,
        'speedmeter_data_global': speedmeter_data_global,
    }
    return render(request, 'main/index.html', context)
