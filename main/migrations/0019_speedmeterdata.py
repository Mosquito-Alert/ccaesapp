# Generated by Django 4.2.1 on 2023-06-01 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_remove_municipalitiesnatcode_year_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpeedMeterData',
            fields=[
                ('version_UUID', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('creation_time', models.DateTimeField()),
                ('nuts_2', models.CharField(blank=True, max_length=4, null=True)),
            ],
        ),
    ]
