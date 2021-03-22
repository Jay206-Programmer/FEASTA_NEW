from django.urls import path
from .views import *

urlpatterns = [
    #mlaas/common/user/login/
    #URL For User Login
    path('common/',CommonClass.as_view()),
    
]