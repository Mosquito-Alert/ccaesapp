import app_config
from django.db import connection
from datetime import datetime
from main.models import ObservationBarChartData, DataUpdateMetadata
from django.utils.timezone import make_aware


def get_ccaa_data(ccaa_code, year):
    cursor = connection.cursor()
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
        END as categoria_mapa,
        date_part('year',marn.observation_date) as anyo,
        left(marn.nuts3_code,4) as ccaa_code
        from
        map_aux_reports_newmap marn,
        nuts_europe ne,
        lau_rg_01m_2018_4326 lrm
        where
        left(marn.nuts3_code,4) = ne.nuts_id and
        nuts_id=%s and marn.lau_code = lrm.gisco_id and
        date_part('year',observation_date) = %s and
        private_webmap_layer in ('mosquito_tiger_probable','mosquito_tiger_confirmed','yellow_fever_probable','yellow_fever_confirmed','japonicus_probable','japonicus_confirmed','culex_probable','culex_confirmed','koreicus_probable','koreicus_confirmed','bite')
        group by date_part('month',marn.observation_date), categoria_mapa, date_part('year',marn.observation_date),left(marn.nuts3_code,4)
        order by 3, 2
    """,(ccaa_code,year,))
    results = cursor.fetchall()
    return results

def load_data():
    this_year = datetime.now().year
    ObservationBarChartData.objects.all().delete()
    cursor = connection.cursor()
    cursor.execute("""
        select nuts_id, name_latn from nuts_europe ne where levl_code = 2 and cntr_code = 'ES' order by 2
    """)
    ccaas = cursor.fetchall()
    to_write = []
    for ccaa in ccaas:
        for year in range(2020,this_year+1):
            _data = get_ccaa_data( ccaa[0], year )
            for d in _data:
                to_write.append(
                    ObservationBarChartData(n=d[0],month=d[1],category=d[2],year=d[3],ccaa_code=d[4])
                )
    ObservationBarChartData.objects.bulk_create(to_write)
    aware_datetime = make_aware(datetime.now())
    try:
        d = DataUpdateMetadata.objects.get(class_name=ObservationBarChartData._meta.verbose_name)
        d.last_update = aware_datetime
    except DataUpdateMetadata.DoesNotExist:
        d = DataUpdateMetadata(class_name=ObservationBarChartData._meta.verbose_name, last_update=aware_datetime)
    d.save()


def main():
    load_data()


if __name__ == '__main__':
    main()
