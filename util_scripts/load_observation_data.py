import app_config

from main.models import ObservationData, DataUpdateMetadata
from django.db import connection
from datetime import datetime
from django.utils.timezone import make_aware

BITE_INDEX = 0
ALBOPICTUS_INDEX = 1
AEGYPTI_INDEX = 2
CULEX_INDEX = 3

def get_bite_data(ccaa_code,year):
    ccaa_param = ccaa_code + '%'
    cursor = connection.cursor()
    cursor.execute("""
        select marn.nuts3_name, marn.lau_name, count(version_uuid) as bites, marn.nuts3_code
        from map_aux_reports_newmap marn,
        (select distinct marn.nuts3_code, nuts3_name, lau_code, lau_name
        from map_aux_reports_newmap marn where marn.nuts3_code ilike %s and marn.nuts3_code is not null and marn.lau_code is not null) as t1
        where "type" = 'bite' and date_part('year',observation_date) = %s and marn.nuts3_code = t1.nuts3_code and marn.lau_code = t1.lau_code group by marn.nuts3_name, marn.lau_name, marn.nuts3_code
    """, (ccaa_param,year,))
    results = cursor.fetchall()
    return results


def get_albopictus_data(ccaa_code,year):
    ccaa_param = ccaa_code + '%'
    cursor = connection.cursor()
    cursor.execute("""
        select marn.nuts3_name, marn.lau_name, count(version_uuid) as n, marn.nuts3_code
        from map_aux_reports_newmap marn,
        (select distinct marn.nuts3_code, nuts3_name, lau_code, lau_name
        from map_aux_reports_newmap marn where marn.nuts3_code ilike %s and marn.nuts3_code is not null and marn.lau_code is not null) as t1
        where type='adult' and date_part('year',observation_date) = %s and (private_webmap_layer = 'mosquito_tiger_probable' or private_webmap_layer = 'mosquito_tiger_confirmed') and
        marn.nuts3_code = t1.nuts3_code and marn.lau_code = t1.lau_code group by marn.nuts3_name, marn.lau_name, marn.nuts3_code
    """, (ccaa_param,year))
    results = cursor.fetchall()
    return results


def get_culex_data(ccaa_code,year):
    ccaa_param = ccaa_code + '%'
    cursor = connection.cursor()
    cursor.execute("""
        select marn.nuts3_name, marn.lau_name, count(version_uuid) as n, marn.nuts3_code
        from map_aux_reports_newmap marn,
        (select distinct marn.nuts3_code, nuts3_name, lau_code, lau_name
        from map_aux_reports_newmap marn where marn.nuts3_code ilike %s and marn.nuts3_code is not null and marn.lau_code is not null) as t1
        where type='adult' and date_part('year',observation_date) = %s and (private_webmap_layer = 'culex_probable' or private_webmap_layer = 'culex_confirmed') and
        marn.nuts3_code = t1.nuts3_code and marn.lau_code = t1.lau_code group by marn.nuts3_name, marn.lau_name, marn.nuts3_code
    """, (ccaa_param,year,))
    results = cursor.fetchall()
    return results


def get_aegypti_data(ccaa_code,year):
    ccaa_param = ccaa_code + '%'
    cursor = connection.cursor()
    cursor.execute("""
        select marn.nuts3_name, marn.lau_name, count(version_uuid) as n, marn.nuts3_code
        from map_aux_reports_newmap marn,
        (select distinct marn.nuts3_code, nuts3_name, lau_code, lau_name
        from map_aux_reports_newmap marn where marn.nuts3_code ilike %s and marn.nuts3_code is not null and marn.lau_code is not null) as t1
        where type='adult' and date_part('year',observation_date) = %s and (private_webmap_layer = 'yellow_fever_probable' or private_webmap_layer = 'yellow_fever_confirmed') and
        marn.nuts3_code = t1.nuts3_code and marn.lau_code = t1.lau_code group by marn.nuts3_name, marn.lau_name, marn.nuts3_code
    """, (ccaa_param,year,))
    results = cursor.fetchall()
    return results


def get_muni_table():
    retval = {}
    cursor = connection.cursor()
    cursor.execute("""
        select
        distinct
        marn.lau_name,
        lrm.lau_id as natcode
        from
        map_aux_reports_newmap marn,
        lau_rg_01m_2018_4326 lrm
        where marn.lau_code  = lrm.gisco_id and marn.nuts3_code ilike 'ES%' and marn.nuts3_code is not null and marn.lau_code is not null
    """)
    results = cursor.fetchall()
    for r in results:
        retval[r[0]] = r[1]
    return retval

def get_provs_munis(ccaa_code):
    ccaa_param = ccaa_code + '%'
    data = {}
    cursor = connection.cursor()
    cursor.execute("""
            select distinct marn.nuts3_code, nuts3_name, lau_code, lau_name
            from map_aux_reports_newmap marn where marn.nuts3_code ilike %s and marn.nuts3_code is not null and marn.lau_code is not null
        """, (ccaa_param,))
    results = cursor.fetchall()
    for r in results:
        r_provincia = r[1]
        r_comarca = r[3]
        try:
            data[r_provincia]
        except KeyError:
            data[r_provincia] = {}
        try:
            data[r_provincia][r_comarca]
        except KeyError:
            data[r_provincia][r_comarca] = [0,0,0,0]
    return data

def get_tabular_data(ccaa_code,year):
    # nuts3 = get_nuts3_ccaa(ccaa_code)
    provs_munis = get_provs_munis(ccaa_code)
    bite_data = get_bite_data(ccaa_code,year)
    albo_data = get_albopictus_data(ccaa_code,year)
    aegy_data = get_aegypti_data(ccaa_code,year)
    culex_data = get_culex_data(ccaa_code,year)

    for b in bite_data:
        data_array = provs_munis[b[0]][b[1]]
        data_array[BITE_INDEX] = b[2]

    for b in albo_data:
        data_array = provs_munis[b[0]][b[1]]
        data_array[ALBOPICTUS_INDEX] = b[2]

    for b in aegy_data:
        data_array = provs_munis[b[0]][b[1]]
        data_array[AEGYPTI_INDEX] = b[2]

    for b in culex_data:
        data_array = provs_munis[b[0]][b[1]]
        data_array[CULEX_INDEX] = b[2]

    data = []
    for provincia in provs_munis:
        for municipi in provs_munis[provincia]:
            dades = provs_munis[provincia][municipi]
            data.append( [ provincia, municipi, dades[BITE_INDEX], dades[ALBOPICTUS_INDEX], dades[AEGYPTI_INDEX], dades[CULEX_INDEX], year ] )
    return data

def get_presence_data():
    retval = {}
    cursor = connection.cursor()
    cursor.execute("""
        select mn.year,mm.natcode,mn.trampeo,mn.ma from main_natcodepresence mn,main_municipalitiesnatcode mm where mn.natmunicipality_id = mm.id
    """)
    results = cursor.fetchall()
    for r in results:
        shortcode = r[1][ len(r[1]) -5: ]
        #retval[r[0]] = {}
        try:
            retval[r[0]]
        except KeyError:
            retval[r[0]] = {}
        retval[r[0]][shortcode] = [r[2], r[3]]
    return retval


def load_data():
    this_year = datetime.now().year
    ObservationData.objects.all().delete()
    cursor = connection.cursor()
    cursor.execute("""
        select ne.nuts_id, ne.nuts_name
        from nuts_europe ne where ne.levl_code = 2 and ne.nuts_id ilike 'ES%';
    """)
    ccaas = cursor.fetchall()
    to_write = []
    muni_table = get_muni_table()
    presence_data = get_presence_data()
    for year in range(2020,this_year+1):
        for ccaa in ccaas:
            print("Loading data for {0} - {1}".format( ccaa, year ))
            ccaa_code = ccaa[0]
            ccaa_name = ccaa[1]
            data = get_tabular_data(ccaa_code,year)
            trampeo = None
            ma = None
            for d in data:
                muni_code = muni_table[d[1]]
                muni_shortcode = muni_code[ len(muni_code) -5: ]
                try:
                    presence_data_year = presence_data[year]
                    presence_data_natcode = presence_data_year[muni_shortcode]
                    trampeo = presence_data_natcode[0]
                    ma = presence_data_natcode[1]
                except KeyError:
                    pass
                to_write.append( ObservationData(
                    ccaa=ccaa_name,
                    ccaa_code=ccaa_code,
                    provincia=d[0],
                    municipi=d[1],
                    n_bite=d[2],
                    n_albo=d[3],
                    n_aegypti=d[4],
                    n_culex=d[5],
                    year=d[6],
                    municipi_code=muni_code,
                    trampeo_albo=trampeo,
                    ma_albo=ma
                ) )
    ObservationData.objects.bulk_create(to_write)
    aware_datetime = make_aware(datetime.now())
    try:
        d = DataUpdateMetadata.objects.get(class_name=ObservationData._meta.verbose_name)
        d.last_update=aware_datetime
    except DataUpdateMetadata.DoesNotExist:
        d = DataUpdateMetadata(class_name=ObservationData._meta.verbose_name, last_update=aware_datetime)
    d.save()

def main():
    load_data()


if __name__ == '__main__':
    main()
