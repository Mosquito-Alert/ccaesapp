import app_config

from main.models import ParticipationData, DataUpdateMetadata
from django.db import connection
from datetime import datetime
from django.utils.timezone import make_aware


def get_ccaa_name_from_code(code):
    cursor = connection.cursor()
    cursor.execute("""
        select name_latn from nuts_europe where nuts_id = %s
    """,(code,))
    result = cursor.fetchone()
    return result[0]


def by_part_value(elem):
    return elem[1]


def get_participation_data_bites(ccaa_code, year):
    ccaa_name = get_ccaa_name_from_code(ccaa_code)
    ccaa_param = ccaa_code + '%'
    cursor = connection.cursor()
    cursor.execute("""
        select count(version_uuid)
        from map_aux_reports_newmap marn
        where marn.private_webmap_layer = 'bite'
        and nuts3_code is not null and nuts3_code ilike %s and date_part('year',observation_date) = %s
    """,(ccaa_param,year))
    result = cursor.fetchone()
    return [ccaa_name,result[0]]


def get_participation_data_sites(ccaa_code,year):
    ccaa_name = get_ccaa_name_from_code(ccaa_code)
    ccaa_param = ccaa_code + '%'
    cursor = connection.cursor()
    cursor.execute("""
        select count(version_uuid)
        from map_aux_reports_newmap marn
        where marn.private_webmap_layer in ('storm_drain_water','breeding_site_other','storm_drain_dry')
        and nuts3_code is not null and nuts3_code ilike %s and date_part('year',observation_date) = %s
    """,(ccaa_param,year,))
    result = cursor.fetchone()
    return [ccaa_name,result[0]]


def get_participation_data_mosquitos(ccaa_code,year):
    ccaa_name = get_ccaa_name_from_code(ccaa_code)
    ccaa_param = ccaa_code + '%'
    cursor = connection.cursor()
    cursor.execute("""
        select count(version_uuid)
        from map_aux_reports_newmap marn
        where marn.private_webmap_layer in ('mosquito_tiger_probable','mosquito_tiger_confirmed','yellow_fever_probable','yellow_fever_confirmed','japonicus_probable','japonicus_confirmed','culex_probable','culex_confirmed','koreicus_probable','koreicus_confirmed')
        and nuts3_code is not null and nuts3_code ilike %s and date_part('year',observation_date) = %s
    """,(ccaa_param,year,))
    result = cursor.fetchone()
    return [ccaa_name,result[0]]


def get_participation_data(year):
    cursor = connection.cursor()
    cursor.execute("""
        select ne.nuts_id, ne.nuts_name
        from nuts_europe ne where ne.levl_code = 2 and ne.nuts_id ilike 'ES%';
    """)
    ccaas = cursor.fetchall()
    total_participation_mosquitos = []
    total_participation_bites = []
    total_participation_sites = []
    for ccaa in ccaas:
        ccaa_code = ccaa[0]
        total_participation_mosquitos.append(get_participation_data_mosquitos(ccaa_code,year))
        total_participation_bites.append(get_participation_data_bites(ccaa_code,year))
        total_participation_sites.append(get_participation_data_sites(ccaa_code,year))
    total_participation_mosquitos.sort(key=by_part_value,reverse=True)
    total_participation_bites.sort(key=by_part_value,reverse=True)
    total_participation_sites.sort(key=by_part_value,reverse=True)
    return {'mosquito':total_participation_mosquitos, 'bite':total_participation_bites, 'site':total_participation_sites}


def load_data():
    this_year = datetime.now().year
    for year in range(2020,this_year+1):
        print("Loading data for year {0}".format(year))
        data = get_participation_data(year)
        to_write = []
        for d in data['bite']:
            to_write.append( ParticipationData( ccaa_name=d[0], n=d[1], category='bite', year=year ) )
        for d in data['site']:
            to_write.append( ParticipationData( ccaa_name=d[0], n=d[1], category='site', year=year ) )
        for d in data['mosquito']:
            to_write.append( ParticipationData( ccaa_name=d[0], n=d[1], category='mosquito', year=year ) )
    ParticipationData.objects.all().delete()
    ParticipationData.objects.bulk_create( to_write )

    aware_datetime = make_aware(datetime.now())
    try:
        d = DataUpdateMetadata.objects.get(class_name=ParticipationData._meta.verbose_name)
        d.last_update = aware_datetime
    except DataUpdateMetadata.DoesNotExist:
        d = DataUpdateMetadata(class_name=ParticipationData._meta.verbose_name, last_update=aware_datetime)
    d.save()


def main():
    load_data()


if __name__ == '__main__':
    main()
