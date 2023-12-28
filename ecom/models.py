from django.db import models


class Product(models.Model):
    name=models.CharField(max_length=40)
    product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
    price = models.PositiveIntegerField()
    description=models.CharField(max_length=40)
    def __str__(self):
        return self.name


# class Orders(models.Model):
#     STATUS =(
#         ('Pending','Pending'),
#         ('Order Confirmed','Order Confirmed'),
#         ('Out for Delivery','Out for Delivery'),
#         ('Delivered','Delivered'),
#     )
#     customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
#     product=models.ForeignKey('Product',on_delete=models.CASCADE,null=True)
#     email = models.CharField(max_length=50,null=True)
#     address = models.CharField(max_length=500,null=True)
#     mobile = models.CharField(max_length=20,null=True)
#     order_date= models.DateField(auto_now_add=True,null=True)
#     status=models.CharField(max_length=50,null=True,choices=STATUS)


class Contact(models.Model):
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    message = models.TextField()
    def __str__(self):
        return f"{self.name} From {self.email}"