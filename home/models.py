from django.db import models
from django.utils.timezone import now


class Contact(models.Model):
     sno= models.AutoField(primary_key=True)
     name= models.CharField(max_length=255)
     email= models.CharField(max_length=100)
     message= models.TextField(null=True,default=now)
     timeStamp=models.DateTimeField(auto_now_add=True, blank=True)
     def __str__(self):
          return "Message from " + self.name + ' - ' + self.email