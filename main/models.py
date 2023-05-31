from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class ParticipationData(models.Model):
    ccaa_name = models.CharField(max_length=150)
    n = models.IntegerField()
    category = models.CharField(max_length=150)
    year = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'participationdata'


class ObservationBarChartData(models.Model):
    n = models.IntegerField()
    month = models.IntegerField()
    category = models.CharField(max_length=150)
    year = models.IntegerField()
    ccaa_code = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'observationbardata'


class ObservationData(models.Model):
    ccaa = models.CharField(max_length=150,null=True)
    ccaa_code = models.CharField(max_length=10,null=True)
    provincia = models.CharField(max_length=150)
    municipi = models.CharField(max_length=150)
    n_bite = models.IntegerField()
    n_albo = models.IntegerField()
    n_aegypti = models.IntegerField()
    n_culex = models.IntegerField()
    n_japonicus = models.IntegerField(null=True)
    n_koreicus = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
    trampeo_albo = models.BooleanField(null=True, blank=True)
    ma_albo = models.BooleanField(null=True, blank=True)
    municipi_code = models.CharField(max_length=150,null=True)

    class Meta:
        verbose_name = 'observationdata'


class NutsEurope(models.Model):
    gid = models.AutoField(primary_key=True)
    nuts_id = models.CharField(max_length=5, blank=True, null=True)
    levl_code = models.SmallIntegerField(blank=True, null=True)
    cntr_code = models.CharField(max_length=2, blank=True, null=True)
    name_latn = models.CharField(max_length=70, blank=True, null=True)
    nuts_name = models.CharField(max_length=106, blank=True, null=True)
    mount_type = models.SmallIntegerField(blank=True, null=True)
    urbn_type = models.SmallIntegerField(blank=True, null=True)
    coast_type = models.SmallIntegerField(blank=True, null=True)
    fid = models.CharField(max_length=5, blank=True, null=True)
    # geom = models.GeometryField(blank=True, null=True)
    europecountry_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nuts_name

    class Meta:
        managed = False
        db_table = 'nuts_europe'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuts = models.ForeignKey(NutsEurope, null=True, on_delete=models.CASCADE, related_name='users_by_nuts')

    def __str__(self):
        nuts_str = "No nuts" if self.nuts is None else self.nuts.nuts_name
        return "{0} - {1}".format(self.user.username, nuts_str)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class DataUpdateMetadata(models.Model):
    class_name = models.CharField(max_length=150, null=True)
    last_update = models.DateTimeField(help_text="Last time model data was updated", null=True, blank=True)


class MunicipalitiesNatCode(models.Model):
    natcode = models.CharField(max_length=11)
    nameunit = models.CharField(max_length=100)
    nuts_2_code = models.CharField(max_length=4)
    nuts_3_code = models.CharField(max_length=5)


class NatCodePresence(models.Model):
    natmunicipality = models.ForeignKey(MunicipalitiesNatCode, on_delete=models.CASCADE)
    trampeo = models.BooleanField()
    ma = models.BooleanField()
    mosquito_class = models.CharField(null=True)
    year = models.IntegerField(null=True)
