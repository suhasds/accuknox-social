from django.urls import path
from django.conf.urls import include

from apps.user.api_views import *

app_name = 'api_urls'

urlpatterns = [
    path('signup', SignUpAPI.as_view(), name="api_signup"),
    path('login', LoginAPI.as_view(), name="api_login"),
    path('logout', LogoutAPI.as_view(), name="api_logout"),
    path('forgot-password', ForgotPasswordAPI.as_view(), name="api_forgot_password"),
    path('change-password', ChangePasswordAPI.as_view(), name="api_change_password"),
    path('profile', GetProfileDetailsAPI.as_view(), name="api_profile"),

]
