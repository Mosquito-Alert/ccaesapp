# Generated by Django 4.2.1 on 2023-05-29 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_dataupdatemetadata'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObservationBarChartData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n', models.IntegerField()),
                ('month', models.IntegerField()),
                ('category', models.CharField(max_length=150)),
                ('year', models.IntegerField()),
                ('ccaa_code', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterModelOptions(
            name='observationdata',
            options={'verbose_name': 'observationdata'},
        ),
        migrations.AlterModelOptions(
            name='participationdata',
            options={'verbose_name': 'participationdata'},
        ),
    ]
