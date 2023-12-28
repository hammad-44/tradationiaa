from django.contrib import admin
from .models import Product, Contact

class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)


class ContactAdmin(admin.ModelAdmin):
    pass
admin.site.register(Contact, ContactAdmin)
