from django.db import models


class Product(models.Model):
    name=models.CharField(max_length=40)
    product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
    price = models.PositiveIntegerField()
    description=models.CharField(max_length=40)
    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    message = models.TextField()
    def __str__(self):
        return f"{self.name} From {self.email}"
    
class ServiceOrders(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    gender = models.CharField(max_length=12)
    service = models.CharField(max_length=50)
    address = models.TextField(null=True)
    notes = models.TextField()
    order_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'From {self.name} For {self.service} On {self.order_time}'
