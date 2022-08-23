from tracemalloc import start
from django.shortcuts import redirect, render
from app.forms import * 
from app.models import *
from app.data import *
from app.file import *
import logging
import json


# Create your views here.



def index(request):
    result = returnresult()
    return render(request, 'index.html',{'result0': result[0],'result1':result[1]})

def dashboardIndex(request):
    dashboard()
    return render(request,'dashboard.html')

def clienteIndex(request):
    pass
    return render(request,'client.html')

def clienteTable(request):
    clientes = Cliente.objects.all().only('nomec','cpf')
    return render(request,'table.html',{'clientes':clientes})

def clienteForm(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/client')
    else:
        form = ClienteForm()
    return render(request,'form.html',{'form':form})

def clienteFormUpdate(request,id):
    cliente = Cliente.objects.get(id=id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST,instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('/client/table')
    else:
        form = ClienteForm(instance=cliente)
    return render(request,'form.html',{'form':form})

def clienteFile(request):
    if request.method == 'POST':
        form = ClienteFile(request.POST,request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            insertDB(request.FILES['file'].name)
            return redirect('/client')   
    else:
        form = ClienteFile()
    return render(request,'file.html',{'form':form})

def clientePreview(request):
    logging.basicConfig(filename='mylog.log', level=logging.DEBUG)
    logging.debug(request)
    values = json.loads(request.GET.get('values'))
    resultado = predict(values)
    return render(request, 'ajax.html', {'resultado': resultado})

def initialize(request):
    startNN()
    result = returnresult()
    return render(request,'index.html',{'result0': result[0],'result1':result[1]})

