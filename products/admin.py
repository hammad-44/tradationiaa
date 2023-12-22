from django.contrib import admin
from .models import ClothProduct, Category , Subcategory,Size,Color
# Register your models here.
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(ClothProduct)