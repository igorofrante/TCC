from tracemalloc import start
from django.shortcuts import redirect, render
from app.forms import * 
from app.models import *
from app.data import *
import logging

# Create your views here.

def index(request):
    return render(request, 'index.html')

def dashboardIndex(request):
    dashboard()
    return render(request,'dashboard.html')

def clienteIndex(request):
    return render(request,'client.html')

def clienteForm(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        logging.basicConfig(filename='mylog.log', level=logging.DEBUG)
        logging.debug(form)
        if form.is_valid():
            form.save()
            return redirect('/client')
    else:
        form = ClienteForm()
    return render(request,'form.html',{'form':form})

def initialize(request):
    result = startNN()
    return render(request,'index.html',{'result0': result[0],'result1':result[1]})

