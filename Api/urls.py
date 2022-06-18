from django.urls import path,include
from Api.views import *


urlpatterns = [

#web urls  home
path('AddUser',AddUser.as_view()),
path('GetSpecificUser',GetSpecificUser.as_view()),

]