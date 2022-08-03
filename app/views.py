from django.shortcuts import redirect, render
from app.forms import * 
from app.models import *

# Create your views here.

def index(request):
    return render(request, 'index.html')

def dashboardIndex(request):
    return render(request,'dashboard.html')

def clienteIndex(request):
    return render(request,'client.html')

