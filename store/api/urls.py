from django.urls import path
from store.api import views

urlpatterns = [
    path('category/', views.CategoryView.as_view(), name='category'),
    path('product/', views.ProductView.as_view(), name='product'),
]
