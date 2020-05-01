from django.contrib import admin
from .models import Anketa
# Register your models here.


class AnketaAdmin(admin.ModelAdmin):
    """
    Register Devices to admin profiles
    """
    list_display = ('name', 'vorname', 'fathername', 'gender',
                    'age', 'urlVK', 'idVK')


admin.site.register(Anketa, AnketaAdmin)
