from django.urls import path
from .views import *

urlpatterns = [
    
    #URL For User Login
    path('auth/login/',UserLoginClass.as_view()),
    path('auth/regestration/',UserRegestrationClass.as_view()),
    path('auth/admin_regestration/',AdminRegestrationClass.as_view()),
    path('verify/<str:unique_id>',verify_user),
    path('auth/get_login_status/',LoginStatusClass.as_view()),
]