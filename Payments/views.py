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
            user = User.objects.create_user(
            email=request.POST['email'],
            name=request.POST['name'],
            password=request.POST['password'])
            return render(request, 'Login.html',{'success': 'Your are successfuly registered Please log in.'})

def index(request):
    if request.method == "POST":
        customer = authenticate(
            email=request.POST['email'], password=request.POST['password'])
        if customer is not None :
            django_login(request, customer)
            return redirect('Dashboard')
        else:
            return render(request, 'Login.html', {'error': 'Your Email or Password are incorrect.'})
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
    received=Transactions.objects.filter(To=request.user.id)
    sent=Transactions.objects.filter(From=request.user.id)
    amount_received=sum([int(trans.Amount)
                                for trans in received])
    amount_sent=sum([int(trans.Amount)
                                for trans in sent])
    return render(request, 'dashboard.html',
    {
    'balance':balance,
    'amount_received':amount_received,
    'amount_sent':amount_sent
    })
    
    
@login_required(login_url='/index')
def Transaction(request):
    allTransaction = Transactions.objects.all().order_by('-id')
    search_query = request.GET.get('search', '')
    if search_query:
        allTransaction = Transactions.objects.filter(
            Q(name__icontains=search_query))
    paginator = Paginator(allTransaction, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Transaction.html', {'allTransaction': allTransaction, 'page_obj': page_obj})
    
    
    

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
    
