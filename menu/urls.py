from django.urls import path
from .views import *

urlpatterns = [
    
    path('menu/add_category/',AddCategoryClass.as_view()),
    path('menu/get_category/',GetCategoryDetailsClass.as_view()),
    path('menu/add_item/',AddItemClass.as_view()),
]