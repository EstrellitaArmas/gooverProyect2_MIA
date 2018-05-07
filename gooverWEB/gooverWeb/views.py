from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

from datetime import datetime, date, time, timedelta
import calendar

from .models import Employee
from .models import Client
from .models import Rol
from .models import MarcaVehiculo
from .models import ModeloVehiculo
from .models import Vehiculo
from .models import Driver
from .models import Reservation

from .forms import EmployeeForm
from .forms import ClientForm
from .forms import LoginForm
from .forms import RolForm
from .forms import MarcaForm
from .forms import ModeloForm
from .forms import VehiculoForm
from .forms import ConductorForm
from .forms import ReservaForm
from django.shortcuts import redirect

def inicio(request):
    request.session['rol'] = ''
    request.session['user'] = ''
    request.session['email'] = ''
    return render(request, 'gooverWeb/inicio.html', {})

def call_dashboard(request):
    if request.session.get('rol') == 'call':
        return render(request, 'gooverWeb/call_dashboard.html', {})
    return render(request, 'gooverWeb/inicio.html', {})

def client_dashboard(request):
    if request.session.get('rol') == 'cliente':
        return render(request, 'gooverWeb/client_dashboard.html', {})

    return render(request, 'gooverWeb/inicio.html', {})

def admin_dashboard(request):
    if request.session.get('rol') == 'admin':
        return render(request, 'gooverWeb/admin_dashboard.html',{})

    return render(request, 'gooverWeb/inicio.html', {})


def admin_list_rol(request):
    if request.session.get('rol') == 'admin':
        roles = Rol.objects.all()
        return render(request, 'gooverWeb/admin_list_rols.html', {'title': 'Lista de roles','roles' : roles})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_list_marca(request):
    if request.session.get('rol') == 'admin':
        marcas = MarcaVehiculo.objects.all()
        return render(request, 'gooverWeb/admin_list_marca.html', {'title': 'Lista de marcas','items' : marcas})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_list_modelo(request):
    if request.session.get('rol') == 'admin':
        modelos = ModeloVehiculo.objects.all()
        return render(request, 'gooverWeb/admin_list_marca.html', {'title': 'Lista de modelos','items' : modelos})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_list_vehiculo(request):
    if request.session.get('rol') == 'admin':
        vehiculos = Vehiculo.objects.all()
        return render(request, 'gooverWeb/admin_list_vehiculo.html', {'title': 'Lista de vehiculos','items' : vehiculos})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_list_conductor(request):
    if request.session.get('rol') == 'admin':
        conductores = Driver.objects.all()
        return render(request, 'gooverWeb/admin_list_conductor.html', {'title': 'Lista de conductores','items' : conductores})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_list_cliente(request):
    if request.session.get('rol') == 'admin':
        clientes = Client.objects.all()
        return render(request, 'gooverWeb/admin_list_cliente.html', {'title': 'Lista de clientes','items' : clientes})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_list_empleado(request):
    if request.session.get('rol') == 'admin':
        empleados = Employee.objects.all()
        return render(request, 'gooverWeb/admin_list_empleado.html', {'title': 'Lista de empleados','items' : empleados})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_reserva(request):
    if request.session.get('rol') == 'admin':
        clientes = Client.objects.all()
        conductores = Driver.objects.all()
        if request.method == "POST":
            new_rol = ReservaForm(request.POST)
            if new_rol.is_valid():
                post = new_rol.save(commit=False)
                ahora = datetime.now()
                print (post.reservation_date)
                #post.reservation_date = ahora
                post.reservation_hour = ahora.hour
                post.payment_method = 'CASH'
                post.status = 'TO_BEGIN'
                post.save()
                return redirect('admin_dashboard')
            else:
                print(new_rol)
                new_rol = RolForm()
                return render(request, 'gooverWeb/admin_reserva.html', {'reserva': new_rol , 'mensaje': 'Rol ya existe'})
        else:
            new_rol = ReservaForm()
        return render(request, 'gooverWeb/admin_reserva.html', {'reserva': new_rol ,
                                                                'clientes' : clientes ,
                                                                'conductores' : conductores})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_rol(request):
    if request.session.get('rol') == 'admin':
        if request.method == "POST":
            new_rol = RolForm(request.POST)
            if new_rol.is_valid():
                post = new_rol.save(commit=False)
                rol_set = Rol.objects.filter(name= post.name)
                if not rol_set.exists():
                    post.save()
                    return redirect('admin_dashboard')
                else:
                    new_rol = RolForm()
                    return render(request, 'gooverWeb/admin_rol.html', {'new_rol': new_rol , 'mensaje': 'Rol ya existe'})
        else:
            new_rol = RolForm()
        return render(request, 'gooverWeb/admin_rol.html', {})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_modelo(request):
    if request.session.get('rol') == 'admin':
        if request.method == "POST":
            new_modelo = ModeloForm(request.POST)
            if new_modelo.is_valid():
                post = new_modelo.save(commit=False)
                marca_set = ModeloVehiculo.objects.filter(nombre= post.nombre)
                if not marca_set.exists():
                    post.save()
                    return redirect('admin_dashboard')
                else:
                    new_modelo = ModeloForm()
                    return render(request, 'gooverWeb/admin_modelo.html', {'new_modelo': new_modelo , 'mensaje': 'Modelo ya existe'})
        else:
            new_modelo = ModeloForm()
        return render(request, 'gooverWeb/admin_modelo.html', {})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_marca(request):
    if request.session.get('rol') == 'admin':
        if request.method == "POST":
            new_marca = MarcaForm(request.POST)
            if new_marca.is_valid():
                post = new_marca.save(commit=False)
                marca_set = MarcaVehiculo.objects.filter(nombre= post.nombre)
                if not marca_set.exists():
                    post.save()
                    return redirect('admin_dashboard')
                else:
                    new_marca = MarcaForm()
                    return render(request, 'gooverWeb/admin_marca.html', {'new_rol': new_marca , 'mensaje': 'Marca ya existe'})
        else:
            new_marca = MarcaForm()

        return render(request, 'gooverWeb/admin_marca.html', {})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_vehiculo(request):
    if request.session.get('rol') == 'admin':
        marcas = MarcaVehiculo.objects.all()
        modelos = ModeloVehiculo.objects.all()
        conductores = Driver.objects.all()
        if request.method == "POST":
            new_marca = VehiculoForm(request.POST)
            if new_marca.is_valid():
                post = new_marca.save(commit=False)
                marca_set = Vehiculo.objects.filter(license_plate= post.license_plate)
                if not marca_set.exists():
                    post.save()
                    return redirect('admin_dashboard')
                else:
                    new_marca = VehiculoForm()
                    return render(request, 'gooverWeb/admin_vehiculo.html',
                                  {'new_vehiculo': new_marca , 'mensaje': 'Placas ya existe',
                                   'marcas': marcas, 'modelos': modelos, 'conductores': conductores

                    })
        else:
            new_marca = VehiculoForm()

        return render(request, 'gooverWeb/admin_vehiculo.html',
                      {'new_vehiculo': new_marca,'marcas': marcas, 'modelos': modelos, 'conductores': conductores
                    })
    return render(request, 'gooverWeb/inicio.html', {})

def admin_conductor(request):
    if request.session.get('rol') == 'admin':
        rols = Rol.objects.all()
        new_conductor = EmployeeForm()
        if request.method == "POST":
            new_conductor = ConductorForm(request.POST)
            if new_conductor.is_valid():
                post = new_conductor.save(commit=False)
                conductor_set = Driver.objects.filter(email= post.email)
                if not conductor_set.exists():
                    post.save()
                    return redirect('admin_dashboard')
                else:
                    new_marca = ConductorForm()
                    return render(request, 'gooverWeb/admin_conductor.html', {'rols' : rols,'new_vehiculo': new_conductor , 'mensaje': 'Placas ya existe'})
        else:
            new_conductor = ConductorForm()

        return render(request, 'gooverWeb/admin_conductor.html', {'rols' : rols, 'new_vehiculo': new_conductor})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_employee(request):
    if request.session.get('rol') == 'admin':
        rols = Rol.objects.all()
        new_employee = EmployeeForm()
        if request.method == "POST":
            new_employee = EmployeeForm(request.POST)
            if new_employee.is_valid():
                post = new_employee.save(commit=False)
                person_set = Employee.objects.filter(email= post.email)
                if not person_set.exists():
                    post.save()
                    return redirect('admin_dashboard')
                else:
                    new_employee = EmployeeForm()
                    return render(request, 'gooverWeb/admin_employee.html', {'rols' : rols , 'new_employee': new_employee , 'mensaje': 'Usuario ya existe con el mismo correo electronico, ingrese uno nuevo'})
            else:
                print("no es valido-------------")
        else:
            new_employee = EmployeeForm()

        return render(request, 'gooverWeb/admin_employee.html', { 'rols' : rols,'new_employee': new_employee})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_cliente(request):
    if request.session.get('rol') == 'admin':
        if request.method == "POST":
            new_client = ClientForm(request.POST)
            if new_client.is_valid():
                post = new_client.save(commit=False)
                person_set = Client.objects.filter(email= post.email)
                if not person_set.exists():
                    post.virtual_cash = 50.0
                    post.save()
                    return redirect('admin_dashboard')
                else:
                    new_client = ClientForm()
                    return render(request, 'gooverWeb/admin_cliente.html', {'new_client': new_client , 'mensaje': 'Usuario ya existe con el mismo correo electronico, ingrese uno nuevo'})
        else:
            new_client = ClientForm()

        return render(request, 'gooverWeb/admin_cliente.html', {'new_client': new_client})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_settings(request):
    if request.session.get('rol') == 'admin':
        if not request.method == "POST":
            try:
                person_set = Employee.objects.get(email=request.session.get('email'))
                return render(request, 'gooverWeb/settings.html', {'user': person_set})
            except Employee.DoesNotExist():
                return redirect('admin_dashboard')
        else:
            new_employee = EmployeeForm(request.POST)
            if new_employee.is_valid():
                post = new_employee.save(commit=False)
                try:
                    person_set = Employee.objects.get(email=post.email)
                    person_set.setName(post.name)
                    person_set.setLast_Name(post.last_name)
                    person_set.setPhone(post.phone)
                    person_set.setAccessKey(post.access_key)
                    person_set.setPhoto(post.photo)
                    person_set.save()
                    request.session['user'] = post.name
                    return render(request, 'gooverWeb/settings.html', {'mensaje': 'Datos guardados con exito', 'user': person_set})
                except Employee.DoesNotExist():
                    return render(request, 'gooverWeb/settings.html', {'mensaje': 'No se puede actualizar' , 'user' : person_set})
            else:
                return render(request, 'gooverWeb/settings.html',{'mensaje': 'No se puede actualizar' })
    return render(request, 'gooverWeb/inicio.html', {})

def client_settings(request):
    if request.session.get('rol') == 'cliente':
        if not request.method == "POST":
            try:
                person_set = Client.objects.get(email=request.session.get('email'))
                return render(request, 'gooverWeb/settings.html', {'user': person_set})
            except Client.DoesNotExist():
                return redirect('client_dashboard')
        else:
            new_employee = ClientForm(request.POST)
            if new_employee.is_valid():
                post = new_employee.save(commit=False)
                try:
                    person_set = Client.objects.get(email=post.email)
                    person_set.setName(post.name)
                    person_set.setLast_Name(post.last_name)
                    person_set.setPhone(post.phone)
                    person_set.setPassword(post.password)
                    person_set.setPhoto(post.photo)
                    person_set.save()
                    request.session['user'] = post.name
                    return render(request, 'gooverWeb/settings.html', {'mensaje': 'Datos guardados con exito', 'user': person_set})
                except Client.DoesNotExist():
                    return render(request, 'gooverWeb/settings.html', {'mensaje': 'No se puede actualizar' , 'user' : person_set})
            else:
                return render(request, 'gooverWeb/settings.html',{'mensaje': 'No se puede actualizar' })
    return render(request, 'gooverWeb/inicio.html', {})

def login(request):
    if request.method == "POST":
        user_login = LoginForm(request.POST)
        if user_login.is_valid():
            post = user_login.save(commit=False)
            person_set = Client.objects.filter(email= post.email, password = post.password) ##Valida si se encuentra en tabla cliente
            if person_set.exists():
                try:
                    person_set = Client.objects.get(email=post.email)
                    request.session['rol'] = 'cliente'
                    request.session['user'] = person_set.getName()
                    request.session['email'] = person_set.getEmail()
                    return redirect('client_dashboard')
                except Client.DoesNotExist():
                    user_login = LoginForm()
            else:
                person_set = Employee.objects.filter(email=post.email, access_key=post.password) ##Valida si se encuentra en tabla empleados
                if person_set.exists():
                    try:
                        person_set = Employee.objects.get(email=post.email)
                        request.session['user'] = person_set.getName()
                        request.session['email'] = person_set.getEmail()
                        if person_set.getRol().getName() == 'Administrador' : # Si es admin
                            request.session['rol'] = 'admin'
                            return redirect('admin_dashboard')
                        elif person_set.getRol().getName() == 'Call Center' : # Si es call center
                            request.session['rol'] = 'call'
                            return redirect('call_dashboard')
                    except Employee.DoesNotExist():
                        user_login = LoginForm()
                        return render(request, 'gooverWeb/login.html', {'new_client': user_login, 'mensaje': 'Usuario o contrasenia invalida'})
                else:
                    user_login = LoginForm()
                    return render(request, 'gooverWeb/login.html', {'new_client': user_login, 'mensaje': 'Usuario o contrasenia invalida'})
    else:
        user_login = LoginForm()

    return render(request, 'gooverWeb/login.html', {})


def registro(request):
    if request.method == "POST":
        new_client = ClientForm(request.POST)
        if new_client.is_valid():
            post = new_client.save(commit=False)
            person_set = Client.objects.filter(email= post.email)
            if not person_set.exists():
                post.virtual_cash = 50.0
                post.save()
                request.session['rol'] = 'cliente'
                request.session['user'] = post.name
                request.session['email'] = post.email
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

