import app_config

from django.contrib.auth.models import User
from main.models import Profile, NutsEurope
from django.db import connection
from slugify import slugify
import string
import random

def generate_password( size=10, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits ):
    return ''.join(random.choice(chars) for _ in range(size))

def load_data():
    User.objects.exclude(is_superuser=True).delete()
    cursor = connection.cursor()
    cursor.execute("""
        select ne.nuts_id, ne.name_latn from nuts_europe ne where ne.cntr_code = 'ES' and ne.levl_code = 2 order by 2
    """)
    results = cursor.fetchall()
    for r in results:
        password = generate_password()
        username = slugify(r[1])
        user = User.objects.create_user(username=username, password=password)
        user.profile.nuts = NutsEurope.objects.get(nuts_id=r[0])
        user.save()
        print("{} - {}".format(username,password))


def main():
    load_data()


if __name__ == '__main__':
    main()
