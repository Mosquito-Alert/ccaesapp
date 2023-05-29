# Generated by Django 4.2.1 on 2023-05-29 06:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_participationdata_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='NutsEurope',
            fields=[
                ('gid', models.AutoField(primary_key=True, serialize=False)),
                ('nuts_id', models.CharField(blank=True, max_length=5, null=True)),
                ('levl_code', models.SmallIntegerField(blank=True, null=True)),
                ('cntr_code', models.CharField(blank=True, max_length=2, null=True)),
                ('name_latn', models.CharField(blank=True, max_length=70, null=True)),
                ('nuts_name', models.CharField(blank=True, max_length=106, null=True)),
                ('mount_type', models.SmallIntegerField(blank=True, null=True)),
                ('urbn_type', models.SmallIntegerField(blank=True, null=True)),
                ('coast_type', models.SmallIntegerField(blank=True, null=True)),
                ('fid', models.CharField(blank=True, max_length=5, null=True)),
                ('europecountry_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'nuts_europe',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nuts', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_by_nuts', to='main.nutseurope')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]