from django.shortcuts import render
from .models import Employee


def inicio(request):
    return render(request, 'gooverWeb/inicio.html', {})


def login(request):
    return render(request, 'gooverWeb/login.html', {})


def registro(request):
    return render(request, 'gooverWeb/registro.html', {})


def post_list(request):
    administrador = Employee.objects.all()
    return render(request, 'gooverWeb/post_list.html', {'posts': administrador})
