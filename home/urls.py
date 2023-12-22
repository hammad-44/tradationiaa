from django.contrib import admin
from django.urls import path
from . import views  

urlpatterns = [
    path('', views.index, name="index"),  
    path('contact', views.contact, name="contact"),  
    path('our-policy', views.our_policy, name="our_policy"),  
    path('privacy-policy', views.privacy_policy, name="privacy_policy"),  
    path('shipping-policy', views.shipping_policy, name="shipping_policy"),  
    path('refund-policy', views.refund_policy, name="refund_policy"),  
    path('terms-conditions', views.terms_conditions, name="terms_conditions"),  
    path('handlelogin', views.handlelogin, name="handlelogin"),  
    path('logouthandle', views.logouthandle, name="logouthandle"),  
    path('signup', views.signup, name="signup"),  
]
