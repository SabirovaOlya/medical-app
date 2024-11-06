from django.urls import path
from .views import ProductListView, ProductDetailView, CartView, PaymentView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/payment/', PaymentView.as_view(), name='payment'),
]
