from . import views
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    # url(r'^accounts/profile/', views.profile, name='tab_account'),
    # url(r'^accounts/changeform/', views.update_profile, name='tab_update'),
    path('', views.main_telemetry_page, name='telemetry_main'),
    path('critical/', views.data_critical, name='telemetry_critical'),
    path('danger/', views.data_attention, name='telemetry_danger'),
    path('get_data/', views.get_data, name='telemetry_get'),
    path('update/', views.update_db, name='telemetry_update'),
    path('all/', views.data_all, name='telemetry_all'),
    path('analyse/', views.display_params, name='telemetry_analyse'),
    path('make_corr/', views.make_correlation, name='telemetry_correlations')
]
