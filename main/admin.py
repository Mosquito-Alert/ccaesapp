from django.contrib import admin
from django.contrib.auth.models import User
from main.models import Profile, NutsEurope, RuntimeSettings

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['nuts'].queryset = NutsEurope.objects.filter(levl_code=2).filter(cntr_code='ES').order_by('nuts_name')
        return super(ProfileAdmin, self).render_change_form(request, context, *args, **kwargs)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(RuntimeSettings)
