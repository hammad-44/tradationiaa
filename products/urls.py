from django.contrib import admin
from django.urls import path
from . import views  

urlpatterns = [
    path('', views.allproducts, name="allproducts"),  
    path('productdetails/', views.productdetails, name="productdetails"),  
    path('checkout/', views.checkout, name="checkout"),  
    path('cart/', views.cart, name="cart"),  
]
