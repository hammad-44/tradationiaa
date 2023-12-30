
from django.contrib import admin
from django.urls import path
from ecom import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),
    path('signin', views.handlelogin,name='signin'),
    path('signup', views.signup , name='signup'),
    path('about', views.aboutus_view),
    path('contactus', views.contactus_view,name='contactus'),
    path('search', views.search_view,name='search'),
    path('logouthandle', views.logouthandle, name="logouthandle"),
    path('order', views.order, name="order"),
    path('products/', views.product, name="product"),
    path('productdetails/<int:pk>', views.productdetails, name="productdetails"),

    path('add-to-cart/<int:pk>', views.add_to_cart_view,name='add-to-cart'),
    path('cart', views.cart_view,name='cart'),
    path('checkout', views.checkout,name='checkout'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart_view,name='remove-from-cart'),


]
