from django.db import models

# Create your models here.

class User(models.Model):

    firstname = models.CharField(max_length=255,default="")
    lastname = models.CharField(max_length=255,default="")
    email = models.EmailField(max_length=255,default="")
    Contactno = models.CharField(max_length=255,default="") 
    password = models.TextField(default="")


    
