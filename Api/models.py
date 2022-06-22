from django.db import models

# Create your models here.

class User(models.Model):

    firstname = models.CharField(max_length=255,default="")
    lastname = models.CharField(max_length=255,default="")
    email = models.EmailField(max_length=255,default="")
    Contactno = models.CharField(max_length=255,default="") 
    password = models.TextField(default="")

class Category(models.Model):

    name = models.CharField(max_length=255,default="")
    userid = models.ForeignKey(User,on_delete =models.CASCADE,blank=True, null=True)
    
