# Generated by Django 4.2.1 on 2023-05-26 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_observationdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='observationdata',
            name='ccaa',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
