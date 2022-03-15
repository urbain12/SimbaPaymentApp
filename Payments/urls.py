from django.urls import path,include
from django.conf.urls import url
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [ 
    path('',index,name='index'),
    path('signup/',signup,name='signup'),
    path('logout/',logout,name='logout'),
    path('Dashboard/',Dashboard,name='Dashboard'),
    path('Transactions/',Transaction,name='Transactions'),
    path('AddTransaction/',AddTransaction,name='AddTransaction'),
    
   ]
