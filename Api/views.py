from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from .models import *
from passlib.hash import django_pbkdf2_sha256 as handler
# Create your views here.


class AddUser(APIView):

    def get(self,request):

        data = User.objects.all().values('firstname','lastname','email','Contactno')

        return Response({"status":True,"data":data},200)

    def post(self,request):
        
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        email = request.data.get('email')
        Contactno = request.data.get('Contactno')
        password = request.data.get('password')

        data = User(firstname=fname,lastname=lname,email=email,Contactno=Contactno,password=handler.hash(password))
        data.save()

        return Response({"status":True,"message":"Account Created Successfully"},201)
        
