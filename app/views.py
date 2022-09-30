from tracemalloc import start
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from app.forms import * 
from app.models import *
from app.data import *
from app.file import *
import logging
import json
from threading import Thread

# Create your views here.

# logging.basicConfig(filename='mylog.log', level=logging.DEBUG)
# logging.debug(request)



def index(request):
    result = returnresult()
    return render(request, 'index.html',{'result0': "{:.2%}".format(result[0]),'result1':"{:.2%}".format(result[1]),'result2':"{:.2%}".format(result[2]),'result3':"{:.2%}".format(result[3])})

def initialize(request):
    print('inicializando')
    startNN()
    print('rede neural executada')
    startLR()
    print('regressao logistica executada')
    return index(request)


###### CLIENTE
refreshResult = False

def clienteIndex(request):
    pass
    return render(request,'client.html')

def clienteTable(request):
    clientes = Cliente.objects.all()
    return render(request,'table.html',{'clientes':clientes})

def refresh(request):
    global refreshResult
    if refreshResult:
        startNN()
        refreshResult = False
    else:
        pass
    return HttpResponse(status = 200) 

def clienteForm(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            global refreshResult
            refreshResult = True
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
            global refreshResult
            refreshResult = True
            return redirect('/client/table')
    else:
        form = ClienteForm(instance=cliente)
    return render(request,'form.html',{'form':form})

def clienteView(request,id):
    cliente = Cliente.objects.get(id=id)
    form = ClienteView(instance=cliente)
    return render(request,'view.html',{'form':form})

def clienteDestroy(request,id):
    cliente = Cliente.objects.get(id=id)
    cliente.delete()
    global refreshResult
    refreshResult = True
    return redirect('/client/table')

def clienteFile(request):
    if request.method == 'POST':
        form = ClienteFile(request.POST,request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            insertDB(request.FILES['file'].name)
            global refreshResult
            refreshResult = True
            return redirect('/client')   
    else:
        form = ClienteFile()
    return render(request,'file.html',{'form':form})

def clientePreview(request):
    print('predizendo')
    values = json.loads(request.GET.get('values'))
    resultado = predict(values)
    print(resultado)
    return render(request, 'ajax.html', {'resultado0': resultado[0], 'resultado1': resultado[1]})

####### DASHBOARD

def dashboardIndex(request):
    dashboard()
    return render(request,'dashboard.html')

