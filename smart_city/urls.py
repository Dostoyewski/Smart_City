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
from django.conf.urls import url, re_path
from allauth.account import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^accounts/', include('allauth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account/login.html')),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='account/logout.html')),
    path('accounts/signup/', auth_views.SignupView.as_view(template_name='account/signup.html')),
    path('accounts/password/change/', auth_views.PasswordChangeView.as_view(template_name=
                                                                            'account/password_change.html')),
    path('accounts/password/set/', auth_views.PasswordSetView.as_view(template_name='account/password_set.html')),
    path('accounts/inactive/', auth_views.AccountInactiveView.as_view(template_name='account/account_inactive.html')),
    path('accounts/email/', auth_views.EmailView.as_view(template_name='account/email.html')),
    path('accounts/confirm-email/', auth_views.ConfirmEmailView.as_view(template_name='account/email_confirm.html')),
    path('accounts/password/reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html')),
    path('accounts/password/reset/done/', auth_views.PasswordResetDoneView.as_view(template_name=
                                                                                   'account/password_reset_done.html')),
    path('accounts/password/reset/key/done/',
         auth_views.PasswordResetFromKeyDoneView.as_view(template_name='account/password_reset_from_key_done.html')),
    path('accounts/password/reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html')),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", auth_views.ConfirmEmailView,
            name="account_confirm_email"),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
            auth_views.PasswordResetFromKeyView,
            name="account_reset_password_from_key"),
]
