from django.shortcuts import render
from django.db import connection
from main.models import ParticipationData, ObservationData
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
    data = [[d.provincia, d.municipi, d.n_bite, d.n_albo, d.n_aegypti, d.n_culex] for d in ObservationData.objects.filter(ccaa_code=ccaa_code).filter(year=year) ]
    return data


def get_participation_data(year):
    total_participation_mosquitos = [[d.ccaa_name, d.n] for d in ParticipationData.objects.filter(category='mosquito').filter(year=year).order_by('-n') ]
    total_participation_sites = [[d.ccaa_name, d.n] for d in ParticipationData.objects.filter(category='site').filter(year=year).order_by('-n')]
    total_participation_bites = [[d.ccaa_name, d.n] for d in ParticipationData.objects.filter(category='bite').filter(year=year).order_by('-n')]
    return {'mosquito': total_participation_mosquitos, 'bite': total_participation_bites, 'site': total_participation_sites}


@login_required
@user_passes_test(lambda u: u.is_superuser)
def index_par(request, ccaa=None, year=None):
    cursor = connection.cursor()
    ccaa_name = get_ccaa_name_from_code(ccaa)
    ccaa_code = ccaa
    year_name = year

    cursor.execute("""
            select count(marn.version_uuid), date_part('month',marn.observation_date) as mes,
            CASE
                WHEN marn.private_webmap_layer = 'mosquito_tiger_probable'
                    THEN 'Mosquito Tigre'
                WHEN marn.private_webmap_layer = 'mosquito_tiger_confirmed'
                    THEN 'Mosquito Tigre'
                WHEN marn.private_webmap_layer = 'yellow_fever_probable'
                    THEN 'Mosquito fiebre amarilla'
                WHEN marn.private_webmap_layer = 'yellow_fever_confirmed'
                    THEN 'Mosquito fiebre amarilla'
                WHEN marn.private_webmap_layer = 'japonicus_probable'
                    THEN 'Mosquito del japón'
                WHEN marn.private_webmap_layer = 'japonicus_confirmed'
                    THEN 'Mosquito del japón'
                WHEN marn.private_webmap_layer = 'culex_probable'
                    THEN 'Mosquito común'
                WHEN marn.private_webmap_layer = 'culex_confirmed'
                    THEN 'Mosquito común'
                WHEN marn.private_webmap_layer = 'koreicus_probable'
                    THEN 'Mosquito de corea'
                WHEN marn.private_webmap_layer = 'koreicus_confirmed'
                    THEN 'Mosquito de corea'
                WHEN marn.private_webmap_layer = 'bite'
                    THEN 'Picaduras'
                ELSE
                    'Otros'
                END as categoria_mapa
                from
                map_aux_reports_newmap marn,
                nuts_europe ne,
                lau_rg_01m_2018_4326 lrm
                where
                left(marn.nuts3_code,4) = ne.nuts_id and
                nuts_id=%s and marn.lau_code = lrm.gisco_id and
                date_part('year',observation_date) = %s and
                private_webmap_layer in ('mosquito_tiger_probable','mosquito_tiger_confirmed','yellow_fever_probable','yellow_fever_confirmed','japonicus_probable','japonicus_confirmed','culex_probable','culex_confirmed','koreicus_probable','koreicus_confirmed','bite')
                group by date_part('month',marn.observation_date), categoria_mapa
                order by 3, 2
        """, (ccaa_code, year_name,))

    dataSet = get_tabular_data(ccaa_code, year_name)
    participation_data = get_participation_data(year_name)

    all_sliced = cursor.fetchall()
    context = {'all_sliced': json.dumps(all_sliced), 'ccaa_name': ccaa_name, 'year_name': year_name,
               'dataSet': json.dumps(dataSet), 'participation_data': json.dumps(participation_data)}
    return render(request, 'main/index.html', context)

# Create your views here.
@login_required
def index(request):
    this_user = request.user
    cursor = connection.cursor()

    nuts = this_user.profile.nuts
    if nuts is None:
        ccaa_name = "Cataluña"
        ccaa_code = 'ES51'
    else:
        ccaa_name = get_ccaa_name_from_code(nuts.nuts_id)
        ccaa_code = nuts.nuts_id
    year_name = 2022
    cursor.execute("""
        select count(marn.version_uuid), date_part('month',marn.observation_date) as mes,
        CASE
            WHEN marn.private_webmap_layer = 'mosquito_tiger_probable'
                THEN 'Mosquito Tigre'
            WHEN marn.private_webmap_layer = 'mosquito_tiger_confirmed'
                THEN 'Mosquito Tigre'
            WHEN marn.private_webmap_layer = 'yellow_fever_probable'
                THEN 'Mosquito fiebre amarilla'
            WHEN marn.private_webmap_layer = 'yellow_fever_confirmed'
                THEN 'Mosquito fiebre amarilla'
            WHEN marn.private_webmap_layer = 'japonicus_probable'
                THEN 'Mosquito del japón'
            WHEN marn.private_webmap_layer = 'japonicus_confirmed'
                THEN 'Mosquito del japón'
            WHEN marn.private_webmap_layer = 'culex_probable'
                THEN 'Mosquito común'
            WHEN marn.private_webmap_layer = 'culex_confirmed'
                THEN 'Mosquito común'
            WHEN marn.private_webmap_layer = 'koreicus_probable'
                THEN 'Mosquito de corea'
            WHEN marn.private_webmap_layer = 'koreicus_confirmed'
                THEN 'Mosquito de corea'
            WHEN marn.private_webmap_layer = 'bite'
                THEN 'Picaduras'
            ELSE
                'Otros'
            END as categoria_mapa
            from
            map_aux_reports_newmap marn,
            nuts_europe ne,
            lau_rg_01m_2018_4326 lrm
            where
            left(marn.nuts3_code,4) = ne.nuts_id and
            nuts_id=%s and marn.lau_code = lrm.gisco_id and
            date_part('year',observation_date) = %s and
            private_webmap_layer in ('mosquito_tiger_probable','mosquito_tiger_confirmed','yellow_fever_probable','yellow_fever_confirmed','japonicus_probable','japonicus_confirmed','culex_probable','culex_confirmed','koreicus_probable','koreicus_confirmed','bite')
            group by date_part('month',marn.observation_date), categoria_mapa
            order by 3, 2
    """,(ccaa_code,year_name,))

    dataSet = get_tabular_data(ccaa_code, year_name)
    participation_data = get_participation_data(year_name)

    all_sliced = cursor.fetchall()
    context = {'all_sliced': json.dumps(all_sliced), 'ccaa_name': ccaa_name, 'year_name': year_name, 'dataSet': json.dumps(dataSet), 'participation_data': json.dumps(participation_data)}
    return render(request, 'main/index.html', context)
