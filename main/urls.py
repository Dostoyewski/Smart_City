from . import views
from django.urls import path

urlpatterns = [
    path('accounts/profile/', views.profile, name='tab_account'),
]