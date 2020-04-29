from django.contrib import admin
from .models import UserProfile
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    """
    Register User Profiles to admin profiles
    """
    list_display = ('user', 'name', 'vorname', 'fathername',
                    'gender', 'age', 'position', 'status', 'exp')


admin.site.register(UserProfile, UserProfileAdmin)