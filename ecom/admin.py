from django.contrib import admin
from .models import Product, Contact, ServiceOrders, Orders

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(ServiceOrders)
admin.site.register(Orders)
