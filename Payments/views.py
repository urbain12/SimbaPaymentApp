import json
from datetime import timedelta
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from dateutil.relativedelta import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *
import requests
import xlwt
import urllib3
import os
from django.contrib import auth
from django.contrib.auth import authenticate, logout as django_logout, login as django_login
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


def signup(request):
    if request.method == 'POST':
        try:
            user1 = User.objects.get(email=request.POST['email'])
            return render(request, 'Login.html', {'error': 'The Email is already Please log in.'})
        except User.DoesNotExist:
            bal= 1000
            user = User.objects.create_user(
            email=request.POST['email'],
            name=request.POST['name'],
            password=request.POST['password'],
            balance =bal)
            return render(request, 'Login.html',{'success': 'Your are successfuly registered Please log in.'})

def index(request):
    if request.method == "POST":
        customer = authenticate(
            email=request.POST['email'], password=request.POST['password'])
        if customer is not None :
            django_login(request, customer)
            return redirect('Dashboard')
        else:
            return render(request, 'Login.html', {'error': 'Your Email or Password are incorrect. '})
    else:
        return render(request, 'Login.html')


# @login_required(login_url='/login')
def logout(request):
    if request.method == 'POST':
        django_logout(request)
    return redirect('index')
    
@login_required(login_url='/index')    
def Dashboard(request):
    userdata = User.objects.get(id=request.user.id)
    balance = userdata.balance
    zar = int(balance*16.52)
    usd =  int(balance*1.11)
    received=Transactions.objects.filter(To=request.user.id)
    sent=Transactions.objects.filter(From=request.user.id)
    amount_received=sum([int(trans.Amount)
                                for trans in received])
    amount_sent=sum([int(trans.Amount)
                                for trans in sent])
    return render(request, 'dashboard.html',
    {
    'balance':balance,
    'zar':zar,
    'usd':usd,
    'amount_received':amount_received,
    'amount_sent':amount_sent
    })
    
    
@login_required(login_url='/index')
def Transaction(request):
    userdata = User.objects.get(id=request.user.id)
    allTransaction = Transactions.objects.filter(From=userdata.id)
    allTransaction1 = Transactions.objects.filter(To=userdata.id)
    usertrans = allTransaction | allTransaction1
    search_query = request.GET.get('search', '')
    if search_query:
        users = User.objects.filter(
            Q(name__icontains=search_query))
        users_ids=[]
        for user in users:
            users_ids.append(user.id)
        alltrans=Transactions.objects.filter(From__in=users_ids)
        alltrans1=Transactions.objects.filter(To__in=users_ids)
        usertrans = alltrans | alltrans1
    paginator = Paginator(usertrans, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Transaction.html', {'usertrans': usertrans, 'page_obj': page_obj})
    
    
    

@login_required(login_url='/login')
def AddTransaction(request):
    if request.method == 'POST':

        user = User.objects.only('id').get(
            id=int(request.POST['user_id']))
        Addtransaction = Transactions()
        Addtransaction.Amount = request.POST['Amount']
        Addtransaction.Currency = request.POST['Currency']
        Addtransaction.To = user
        Addtransaction.From = request.user
        Addtransaction.save()
        user.balance= user.balance + int(request.POST['Amount'])
        user.save()
        sender=User.objects.get(id=request.user.id)
        sender.balance=sender.balance-int(request.POST['Amount'])
        sender.save()
        # Addcustomers=True
        return redirect('Transactions')
    else:
        userdata = User.objects.get(id=request.user.id)
        balance = userdata.balance
        users=User.objects.exclude(id = request.user.id)
        return render(request,'addTransaction.html',{'users':users,'balance':balance})



@login_required(login_url='/login')
def changeuserpassword(request, userID):
    if request.method == 'POST':
        if request.POST['newpassword'] == request.POST['confirmpassword']:
            user = User.objects.get(id=userID)
            if user.check_password(request.POST['password']):
                password = request.POST['newpassword']
                user.set_password(password)
            user.save()
            return redirect('index')
        else:
            alert = True
            return render(request, 'Changepassword.html', {'alert': alert})
    else:
        alert = False
        return render(request, 'Changepassword.html', {'alert': alert})
    
