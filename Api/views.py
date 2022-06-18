from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from .models import *
from passlib.hash import django_pbkdf2_sha256 as handler
# Create your views here.
import Api.usable as uc

class AddUser(APIView):

    def get(self,request):

        try:

            data = User.objects.all().values('id','firstname','lastname','email','Contactno').order_by('-id')
            return Response({"status":True,"data":data},200)

        except Exception as e:
            message = {'status':'error','message':str(e)}
            return Response(message)

    def post(self,request):

        try:
        
            fname = request.data.get('fname')
            lname = request.data.get('lname')
            email = request.data.get('email')
            Contactno = request.data.get('Contactno')
            password = request.data.get('password')

            if uc.checkemailforamt(email):

                if not uc.passwordLengthValidator(password):

                
                    return Response({"status":False,"message":"Password should not be less than 8 or greater than 20"},422)

                checkemail = User.objects.filter(email = email).first()
                if checkemail:

                    return Response({"status":False,"message":"Email Already Exist"},409)


                data = User(firstname=fname,lastname=lname,email=email,Contactno=Contactno,password=handler.hash(password))
                data.save()

                return Response({"status":True,"message":"Account Created Successfully"},201)

            

            else:
                return Response({"status":False,"message":"Email format is incorrect"},422)

        except Exception as e:
            message = {'status':'error','message':str(e)}
            return Response(message)

    def delete(self,request):

        try:

            id = request.GET['id']
            data = User.objects.filter(id=id).first()
            if data:
                data.delete()
                return Response({"status":True,"message":"Data Deleted Successfully"},200)

            else:
                return Response({"status":False,"message":"Data not found"},404)

        except Exception as e:
            message = {'status':'error','message':str(e)}
            return Response(message)


    def put(self,request):

        try:

            id = request.data.get('id')
            fname = request.data.get('fname')
            lname = request.data.get('lname')
            Contactno = request.data.get('Contactno')
            password = request.data.get('password')

            

            checkuser = User.objects.filter(id = id).first()
            if checkuser:

                checkuser.firstname = fname
                checkuser.lastname = lname
                checkuser.Contactno = Contactno

                if password != "nochange":

                    if not uc.passwordLengthValidator(password):

                        return Response({"status":False,"message":"Password should not be less than 8 or greater than 20"},422)
                        
                    checkuser.password = handler.hash(password)


                checkuser.save()

                return Response({"status":True,"message":"Update Successfully"},201)


            
            else:
                return Response({"status":False,"message":"Data not found"},404)

        except Exception as e:
            message = {'status':'error','message':str(e)}
            return Response(message)

class GetSpecificUser(APIView):

    def get(self,request):

        try:
            id = request.GET['id']
            data = User.objects.filter(id=id).values('id','firstname','lastname','email','Contactno').first()
            if data:
                return Response({"status":True,"data":data},200)

            else:
                return Response({"status":False,"message":"Data not found"},404)


        except Exception as e:
            message = {'status':'error','message':str(e)}
            return Response(message)

