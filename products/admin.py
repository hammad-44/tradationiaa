from django.contrib import admin
from .models import ClothProduct, Category , Subcategory
# Register your models here.
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(ClothProduct)