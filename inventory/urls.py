from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.item_list, name="item-List"),
    path('items/create', views.create_item, name="create-item"),
    path('categories', views.create_category, name='create-category'),
]