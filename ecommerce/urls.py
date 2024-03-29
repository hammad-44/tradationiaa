
from django.contrib import admin
from django.urls import path
from ecom import views

admin.site.site_header="Traditioniaa Admin "
admin.site.site_title="Traditioniaa Admins Panel"
admin.site.index_title="Welcome to Traditioniaa Admin Panel"



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),
    path('signin', views.handlelogin,name='signin'),
    path('signup', views.signup , name='signup'),
    path('about', views.aboutus_view),
    path('contactus', views.contactus_view,name='contactus'),
    path('privacypolicy', views.privacypolicy,name='privacypolicy'),
    path('returnpolicy', views.returnpolicy,name='returnpolicy'),
    path('search', views.search_view,name='search'),
    path('logouthandle', views.logouthandle, name="logouthandle"),
    path('order', views.order, name="order"),
    path('products/', views.product, name="product"),
    path('products/<slug:catogory>', views.product, name="product"),
    path('productdetails/<int:pk>', views.productdetails, name="productdetails"),

    path('add-to-cart/<int:pk>', views.add_to_cart_view,name='add-to-cart'),
    path('cart', views.cart_view,name='cart'),
    path('checkout/', views.checkout,name='checkout'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart_view,name='remove-from-cart'),


]
