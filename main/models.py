from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class ParticipationData(models.Model):
    ccaa_name = models.CharField(max_length=150)
    n = models.IntegerField()
    category = models.CharField(max_length=150)
    year = models.IntegerField(null=True)


class ObservationData(models.Model):
    ccaa = models.CharField(max_length=150,null=True)
    ccaa_code = models.CharField(max_length=10,null=True)
    provincia = models.CharField(max_length=150)
    municipi = models.CharField(max_length=150)
    n_bite = models.IntegerField()
    n_albo = models.IntegerField()
    n_aegypti = models.IntegerField()
    n_culex = models.IntegerField()
    year = models.IntegerField(null=True)


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
