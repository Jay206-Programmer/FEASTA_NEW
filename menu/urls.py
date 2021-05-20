from django.urls import path
from .views import *

urlpatterns = [
    
    path('menu/add_category/',AddCategoryClass.as_view()),
    path('menu/get_category/',GetCategoryDetailsClass.as_view()),
    path('menu/add_item/',AddItemClass.as_view()),
    path('menu/update_item/',UpdateItem.as_view()),
    path('menu/get_item/',GetItemDetailsClass.as_view()),
    path('menu/place_order/',AddCartClass.as_view()),
    path('menu/get_cart/',GetCartsDetailsClass.as_view()),
    path('menu/set_cart/',SetOrderState.as_view()),
]