from django.urls import path
from .views import *

urlpatterns = [
    
    path('menu/add_category/',AddCategoryClass.as_view()),
]