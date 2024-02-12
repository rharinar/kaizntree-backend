from django.urls import path
from . import views

urlpatterns = [
    # path('hello/', views.say_hello),
    # path('users', views.UserListCreate.as_view(), name="Create-User-List"),
    # path('user/<int:pk>/', views.UserRetrieveUpdateDelete.as_view(), name="user-details"),
    # path('categories', views.CategoryListCreate.as_view(), name="Create-category-List"),
    # path('category/<int:pk>/', views.CategoryRetrieveUpdateDelete.as_view(), name="category-details"),
    # path('snippets/', views.SnippetList.as_view()),
    # path('items/', views.itemListView.as_view(), name="item-List"),
    path('items/', views.itemList, name="item-List"),
    path('items/create', views.create_item, name="create-item"),
    path('categories', views.create_category, name='create-category'),
    # path('item/<int:pk>/', views.ItemRetrieveUpdateDelete.as_view(), name="item-details")
]