# Generated by Django 4.2.1 on 2023-06-14 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_observationdata_ma_japo_observationdata_trampeo_japo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='accepted_terms',
            field=models.BooleanField(default=False),
        ),
    ]
