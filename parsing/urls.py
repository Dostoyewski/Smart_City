from . import views
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    path('enter_data/', views.make_parsing, name='parsing_enter')
]