from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from .models import *
from passlib.hash import django_pbkdf2_sha256 as handler
# Create your views here.
import Api.usable as uc
import jwt
import datetime
from decouple import config

class AddUser(APIView):

    def get(self,request):

        try:

            data = User.objects.all().values('id','name','lastname','email','Contactno').order_by('-id')
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

                data = {'firstname':fname,'lastname':lname,'Email':email,'Contactno':Contactno}

                return Response({"status":True,"message":"Account Created Successfully","data":data},201)

            

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

class AddCategory(APIView):

    def post(self,request):

        name = request.data.get('name')
        userid = request.data.get('userid')

        userobj = User.objects.filter(id =userid).first()
        if userobj:
        
            data = Category(name=name,userid=userobj)
            data.save()

            return Response({"status":True,"message":"Add Category Successfully"},201)

        else:
            return Response({"status":False,"message":"User Not Found"},404)

    def get(self,request):

        id = request.GET['id']

        data = Category.objects.filter(userid__id=id).values('id','name').order_by('-id')
        if data:
            return Response({"status":True,"data":data},200)

        else:
            return Response({"status":False,"message":"Data not found"},404)

class UserLogin(APIView):

    def get(self,request):

     
        my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:

            data = User.objects.all().values('id','firstname','lastname','email','Contactno').order_by('-id')
            return Response({"status":True,"data":data},200)

        else:
            return Response({'status':False,'message':'Unauthorized'},status=401)

    def post(self,request):
        
     
        email = request.data.get('email')
        password = request.data.get('password')

        fetchUser = User.objects.filter(email=email).first()
        if fetchUser:

            if handler.verify(password,fetchUser.password):

                access_token_payload = {
                    'id': fetchUser.id,
                    'name': fetchUser.firstname+fetchUser.lastname,
                    'email':fetchUser.email,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                    'iat': datetime.datetime.utcnow(),

                }
                access_token = jwt.encode(access_token_payload,config('userkey'), algorithm='HS256')

                data = {'firstname':fetchUser.firstname,'lastname':fetchUser.lastname,'Email':fetchUser.email,'Contactno':fetchUser.Contactno}
                return Response({"status":True,"message":"Login Successfully","token":access_token,"userdata":data},200)

            else:
                return Response({"status":False,"message":"Invalid Credientials"},401)
            
        
        else:
            return Response({"status":False,"message":"Account Doesnot Exist"},404)



    

  