import app_config
import csv
import os
from pathlib import Path
from main.models import NatCodePresence, MunicipalitiesNatCode

BASE_DIR = Path(__file__).resolve().parent.parent


def load_data(year):
    to_write = []
    with open(os.path.join(BASE_DIR, 'util_scripts/PresenciaTigre.csv')) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            try:
                natmunicipality = MunicipalitiesNatCode.objects.get(natcode=row[0])
                trampeo = True if row[2] == '1' else False
                ma = True if row[3] == '1' else False
                to_write.append(NatCodePresence( natmunicipality=natmunicipality, trampeo=trampeo, ma=ma, mosquito_class="albopictus", year=year))
            except MunicipalitiesNatCode.DoesNotExist:
                print("Municipality with code {0} does not exist".format(row[0]))

    NatCodePresence.objects.filter(year=year).delete()
    NatCodePresence.objects.bulk_create(to_write)


def main():
    load_data(2022)


if __name__ == '__main__':
    main()
