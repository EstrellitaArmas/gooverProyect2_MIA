from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Employee
from .models import Client
from .forms import ClientForm
from .forms import LoginClientForm
from django.shortcuts import redirect


def inicio(request):
    return render(request, 'gooverWeb/inicio.html', {})


def login(request):
    if request.method == "POST":
        new_client = LoginClientForm(request.POST)
        if new_client.is_valid():
            post = new_client.save(commit=False)
            person_set = Client.objects.filter(email= post.email, password = post.password)
            if person_set.exists():
                try:
                    person_set = Client.objects.get(email=post.email)
                    parameters = {'user': person_set.getName(), 'mensaje': 'Bienvenido' + person_set.getName()}
                    return render(request, 'gooverWeb/client_dashboard.html', parameters )
                    #return redirect('client_dashboard')
                except Client.DoesNotExist():
                    new_client = LoginClientForm()
                    return render(request, 'gooverWeb/login.html',
                                  {'new_client': new_client, 'mensaje': 'Usuario o contrasenia invalida'})
            else:
                new_client = LoginClientForm()
                return render(request, 'gooverWeb/login.html', {'new_client': new_client, 'mensaje': 'Usuario o contrasenia invalida'})
    else:
        new_client = LoginClientForm()

    return render(request, 'gooverWeb/login.html', {})


def client_dashboard(request):
    return render(request, 'gooverWeb/client_dashboard.html', {})


def registro(request):
    if request.method == "POST":
        new_client = ClientForm(request.POST)
        if new_client.is_valid():
            post = new_client.save(commit=False)
            person_set = Client.objects.filter(email= post.email)
            if not person_set.exists():
                post.virtual_cash = 50.0
                post.save()
                return redirect('client_dashboard')
            else:
                new_client = ClientForm()
                return render(request, 'gooverWeb/registro.html', {'new_client': new_client , 'mensaje': 'Usuario ya existe con el mismo correo electronico, ingrese uno nuevo'})
    else:
        new_client = ClientForm()

    return render(request, 'gooverWeb/registro.html', {'new_client': new_client})


def post_list(request):
    administrador = Employee.objects.all()
    return render(request, 'gooverWeb/post_list.html', {'posts': administrador})

