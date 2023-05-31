import app_config
import json
import os
from pathlib import Path
from main.models import MunicipalitiesNatCode


BASE_DIR = Path(__file__).resolve().parent.parent


def load_data():
    datafile = open( os.path.join(BASE_DIR, 'util_scripts/spain-municipalities.json'), "r")
    string_json = datafile.read()
    json_json = json.loads(string_json)
    to_write = []
    for d in json_json['objects']['municipalities']['geometries']:
        print(d['properties'])
        elem = d['properties']
        to_write.append(
            MunicipalitiesNatCode(
                natcode=elem['NATCODE'],
                nameunit=elem['NAMEUNIT'],
                nuts_2_code=elem['CODNUT2'],
                nuts_3_code=elem['CODNUT3']
            )
        )
    MunicipalitiesNatCode.objects.all().delete()
    MunicipalitiesNatCode.objects.bulk_create(to_write)



def main():
    load_data()


if __name__ == '__main__':
    main()

