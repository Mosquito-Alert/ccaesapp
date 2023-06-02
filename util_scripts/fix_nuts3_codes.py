import app_config
import json
import os
from pathlib import Path
from main.models import MunicipalitiesNatCode
from django.db import connection


def do_work():
    cursor = connection.cursor()
    cursor.execute(
        """
        update map_aux_reports_newmap nm set nuts3_code = subquery.loccode from
        (select version_uuid, fl.loccode, fl.locname
        from map_aux_reports_newmap marn, fine_limits fl
        where fl.codelevel = 3 and fl.cntrycode = 'ES' and st_contains(geom,st_setsrid(st_point(marn.lon,marn.lat),4326))) as subquery
        where nm.version_uuid = subquery.version_uuid;
        """
    )
    cursor.execute(
        """
        update map_aux_reports_newmap nm set nuts3_name = subquery.nuts_name from
        ( select nuts_id, nuts_name from nuts_europe where levl_code = 3 and nuts_id like 'ES%' ) as subquery
        where subquery.nuts_id = nm.nuts3_code;
        """
    )


def main():
    do_work()


if __name__ == '__main__':
    main()
