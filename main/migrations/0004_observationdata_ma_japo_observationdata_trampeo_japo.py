# Generated by Django 4.2.1 on 2023-06-12 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_municipalitiesnatcode_lau_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='observationdata',
            name='ma_japo',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='observationdata',
            name='trampeo_japo',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
