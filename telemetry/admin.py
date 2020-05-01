from django.contrib import admin
from .models import Device, StatData, Approx
# Register your models here.


class DeviceAdmin(admin.ModelAdmin):
    """
    Register Devices to admin profiles
    """
    list_display = ('idDevice', 'string', 'danger_temp', 'critical_temp',
                    'danger_vibr', 'critical_vibr', 'danger_pow', 'critical_pow',
                    'danger_load', 'critical_load', 'danger_time', 'critical_time')


class StatAdmin(admin.ModelAdmin):
    """
    Register StatData to admin profiles
    """
    list_display = ('device', 'date', 'temp', 'vibration', 'load', 'time')


class ApproxAdmin(admin.ModelAdmin):
    """
    Register approximation to admin profiles
    """
    list_display = ('device', 'param', 'piers', 'array')


admin.site.register(Device, DeviceAdmin)
admin.site.register(Approx, ApproxAdmin)
admin.site.register(StatData, StatAdmin)
