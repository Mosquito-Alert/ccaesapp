# Generated by Django 4.2.1 on 2023-05-26 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_observationdata_ccaa'),
    ]

    operations = [
        migrations.AddField(
            model_name='observationdata',
            name='ccaa_code',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
