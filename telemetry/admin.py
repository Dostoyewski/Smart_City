from django.contrib import admin
from .models import Device
# Register your models here.


class DeviceAdmin(admin.ModelAdmin):
    """
    Register User Profiles to admin profiles
    """
    list_display = ('idDevice', 'string', 'danger_temp', 'critical_temp',
                    'danger_vibr', 'critical_vibr', 'danger_pow', 'critical_pow',
                    'danger_load', 'critical_load', 'danger_time', 'critical_time')


admin.site.register(Device, DeviceAdmin)