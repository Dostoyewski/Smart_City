from . import views
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    #url(r'^accounts/profile/', views.profile, name='tab_account'),
    #url(r'^accounts/changeform/', views.update_profile, name='tab_update'),
    path('', views.main_telemetry_page, name='telemetry_main'),
    path('critical/', views.data_critical, name='telemetry_critical'),
    path('danger/', views.data_attention, name='telemetry_danger'),
    path('all/', views.data_all, name='telemetry_all'),
    path('update/', views.update_db, name='telemetry_update')
]