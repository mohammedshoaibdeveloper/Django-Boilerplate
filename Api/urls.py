from django.urls import path,include
from Api.views import *


urlpatterns = [

#web urls  home
path('index',index.as_view()),

]