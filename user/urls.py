from django.urls import path
from .views import (
    user_register_view,
    user_login_view,
    user_logout_view,
    favorites_view,
    verify_otp_view,
    resend_otp_view,

)




urlpatterns = [

    path('register/', user_register_view, name='user_register'),
    path('login/', user_login_view, name='user_login'),
    path('logout/', user_logout_view, name='logout'),
    path('favorites/', favorites_view, name='favorites'),
    path('verify-otp/', verify_otp_view, name='verify_otp'),
    path('resend-otp/', resend_otp_view, name='resend_otp'),

]
