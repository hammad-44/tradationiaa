from django.apps import AppConfig
from django.db.models import BigAutoField

class EcomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecom'
