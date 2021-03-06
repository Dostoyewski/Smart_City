"""Smart_City URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from allauth.account import views as auth_views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from main.views import mapi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('telemetry/', include('telemetry.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^webpush/', include('webpush.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account/login.html'),
         name="account_login"),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'),
         name="account_logout"),
    path('accounts/signup/', auth_views.SignupView.as_view(template_name='account/signup.html'),
         name="account_signup"),
    path('accounts/password/change/', auth_views.PasswordChangeView.as_view(template_name=
                                                                            'account/password_change.html'),
         name="account_change_password"),
    path('accounts/password/set/', auth_views.PasswordSetView.as_view(template_name='account/password_set.html'),
         name="account_set_password"),
    path('accounts/inactive/', auth_views.AccountInactiveView.as_view(template_name='account/account_inactive.html'),
         name="account_inactive"),
    path('accounts/email/', auth_views.EmailView.as_view(template_name='account/email.html'),
         name="account_email"),
    path('accounts/confirm-email/', auth_views.ConfirmEmailView.as_view(template_name='account/email_confirm.html'),
         name="account_email_verification_sent"),
    path('accounts/password/reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'),
         name="account_reset_password"),
    path('accounts/password/reset/done/', auth_views.PasswordResetDoneView.as_view(template_name=
                                                                                   'account/password_reset_done.html'),
         name="account_reset_password_done"),
    path('accounts/password/reset/key/done/',
         auth_views.PasswordResetFromKeyDoneView.as_view(template_name='account/password_reset_from_key_done.html'),
         name="account_reset_password_from_key_done"),
    path('sw.js', TemplateView.as_view(template_name='main/sw.js', content_type='application/x-javascript')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('djeym/', include('djeym.urls', namespace='djeym')),
    path('map/', mapi, name='mapi'),
    path('parsing/', include('parsing.urls')),
] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
) + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

