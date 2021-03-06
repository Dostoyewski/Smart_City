from . import views
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    url(r'^accounts/profile/', views.profile, name='tab_account'),
    url(r'^accounts/changeform/', views.update_profile, name='tab_update'),
    path('send_push', views.send_push, name='send_push'),
    path('', views.home, name='home'),
]
