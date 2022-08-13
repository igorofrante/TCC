from tracemalloc import start
from django.shortcuts import redirect, render
from app.forms import * 
from app.models import *
from app.data import *

# Create your views here.

def index(request):
    return render(request, 'index.html')

def dashboardIndex(request):
    dashboard()
    return render(request,'dashboard.html')

def clienteIndex(request):
    return render(request,'client.html')

def initialize(request):
    result = startNN()
    return render(request,'index.html',{'result0': result[0],'result1':result[1]})

