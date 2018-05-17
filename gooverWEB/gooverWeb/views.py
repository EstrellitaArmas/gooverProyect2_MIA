import operator
from django.db import connection
from django.shortcuts import render, render_to_response, get_object_or_404

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
from .forms import ReservaEditForm
from .forms import ReservaConsultaForm
from .forms import ReservaConsultaHistoriaForm
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
        try:
            ########################top clientes #######################
            clientes = Client.objects.all()
            resultados= {}
            for item in clientes:
                reservas = Reservation.objects.filter(client_id=item.id)
                total = 0
                for item_r in reservas:
                    total += item_r.price
                resultados[item.name] = [float(total)]
            resultado = sorted(resultados.items(), key=operator.itemgetter(1))
            resultado.reverse()
            ########################top conductores #######################
            drivers = Driver.objects.all()
            resultados = {}
            for item in drivers:
                reservas = Reservation.objects.filter(conductor_id=item.id)
                total = 0
                for item_r in reservas:
                    total += item_r.price
                resultados[str(item.name)] = [float(total)]
            conductores = sorted(resultados.items(), key=operator.itemgetter(1))
            conductores.reverse()
            ######################## consulta por fecha #######################
            if request.method == "POST":
                form = ReservaConsultaForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    try:
                        reservas = Reservation.objects.filter(reservation_date=post.reservation_date)
                        total = 0
                        for item_r in reservas:
                            total += item_r.price
                    except Reservation.DoesNotExist():
                        ahora = datetime.now()
                        reservas = Reservation.objects.filter(reservation_date=ahora.today())
                        total = 0
                        for item_r in reservas:
                            total += item_r.price
                else:
                    ahora = datetime.now()
                    reservas = Reservation.objects.filter(reservation_date=ahora.today())
                    total = 0
                    for item_r in reservas:
                        total += item_r.price
            else:
                ahora = datetime.now()
                reservas = Reservation.objects.filter(reservation_date=ahora.today())
                total = 0
                for item_r in reservas:
                    total += item_r.price
            ######################## historial #######################
            conductores_list = Driver.objects.all()
            if request.method == "POST":
                form = ReservaConsultaHistoriaForm(request.POST)
                conductores_list = Driver.objects.all()
                if form.is_valid():
                    post = form.save(commit=False)
                    try:
                        historia = Reservation.objects.filter(conductor_id=post.conductor_id).order_by('reservation_date')

                    except Reservation.DoesNotExist():
                        historia = {}
                else:
                    historia = {}
            else:
                historia = {}
            ######################## graficas #################################
            cancelados = 0
            completados = 0
            efectivo = 0
            tarjeta = 0
            moneda = 0
            sql = "SELECT COUNT(*) , R.STATUS  FROM GOOVERWEB_RESERVATION R WHERE (R.STATUS = 'CANCELED' OR R.STATUS = 'COMPLETE') AND extract(month from R.RESERVATION_DATE) =  %s GROUP BY R.STATUS;"
            cursor = connection.cursor()
            if request.method == "POST":
                form = ReservaConsultaForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    cursor.execute(sql,[post.reservation_date.month])
                else:
                    cursor = connection.cursor()
                    cursor.execute(sql, [ahora.month])

            else:
                cursor = connection.cursor()
                cursor.execute(sql, [ahora.month])

            rows = cursor.fetchall()
            cuenta = [row[1] for row in rows]
            if (cuenta.count('COMPLETE') > 0):
                cuenta = [row[0] for row in rows]
                cancelados = cuenta[0]
                completados = cuenta[1]
            elif (cuenta.count('COMPLETE') == 0 and cuenta.count('CANCELED') == 0):
                cancelados = 0
                completados = 0
            else:
                cuenta = [row[0] for row in rows]
                cancelados = cuenta[0]

            sql = "SELECT COUNT(*), R.PAYMENT_METHOD FROM GOOVERWEB_RESERVATION R WHERE (R.PAYMENT_METHOD = 'CASH' OR R.PAYMENT_METHOD = 'CARD' OR R.PAYMENT_METHOD ='VIRTUAL') GROUP BY R.PAYMENT_METHOD;";
            cursor = connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            metodos = [row[0] for row in rows]
            moneda = metodos[0]
            efectivo = metodos[1]
            tarjeta = metodos[2]

            ##########################################################
            return render(request, 'gooverWeb/admin_dashboard.html', {'resultados':resultado[0:10] ,
                                                                      'conductores' : conductores[0:10],
                                                                      'reservas':reservas, 'total' : total,
                                                                      'historia':historia, 'conductores_list' : conductores_list,
                                                                      'cancelados': cancelados, 'completados':completados,
                                                                      'efectivo':efectivo,'tarjeta':tarjeta,'moneda':moneda })
        except Client.DoesNotExist():
            items = Client.objects.all()
            return render(request, 'gooverWeb/admin_dashboard.html', {})


    return render(request, 'gooverWeb/inicio.html', {})
#########################################
def admin_list_rol(request):
    if request.session.get('rol') == 'admin':
        roles = Rol.objects.all()
        return render(request, 'gooverWeb/admin_list_rols.html', {'title': 'Lista de roles','roles' : roles})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_edit_rol(request,id):
    if request.session.get('rol') == 'admin':
        post = get_object_or_404(Rol, id=id)
        if request.method == "POST":
            form = RolForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                try:
                    person_set = Rol.objects.get(id=id)
                    person_set.name = post.name
                    person_set.description = post.description
                    person_set.save()
                    return redirect('admin_list_rol')
                except Reservation.DoesNotExist():
                    return render(request, 'gooverWeb/admin_list_rol.html', {'mensaje': 'No se puede actualizar' })

        else:
            form = RolForm(instance=post)
        return render(request, 'gooverWeb/admin_edit_rol.html', {'form': form})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_delete_rol(request,id):
    if request.session.get('rol') == 'admin':
        if request.method != "POST":
            try:
                person_set = Rol.objects.get(id=id)
                person_set.delete()
                return redirect('admin_list_rol')
            except Rol.DoesNotExist():
                return render(request, 'gooverWeb/admin_list_rol.html', {'mensaje': 'No se puede actualizar' })
        else:
            return redirect('admin_list_rol')
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

#########################################
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

#########################################
def admin_list_conductor(request):
    if request.session.get('rol') == 'admin':
        conductores = Driver.objects.all()
        return render(request, 'gooverWeb/admin_list_conductor.html', {'title': 'Lista de conductores','items' : conductores})
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

def admin_edit_conductor(request,id):
    if request.session.get('rol') == 'admin':
        post = get_object_or_404(Driver, id=id)
        if request.method == "POST":
            form = ConductorForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                try:
                    person_set = Driver.objects.get(id=id)
                    person_set.name = post.name
                    person_set.last_name= post.last_name
                    person_set.phone = (post.phone)
                    person_set.access_key = (post.access_key)
                    person_set.photo = (post.photo)
                    person_set.email = post.email
                    person_set.photo_license = post.photo_license
                    person_set.save()
                    return redirect('admin_list_conductor')
                except Driver.DoesNotExist():
                    conductores = Driver.objects.all()
                    return render(request, 'gooverWeb/admin_list_conductor.html', {'title': 'Lista de conductores',
                                                                                   'items' : conductores,
                                                                                   'mensaje': 'No se puede actualizar' })

        else:
            form = ConductorForm(instance=post)
        return render(request, 'gooverWeb/admin_edit_conductor.html', {'form': form})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_delete_conductor(request,id):
    if request.session.get('rol') == 'admin':
        if request.method != "POST":
            try:
                person_set = Driver.objects.get(id=id)
                person_set.delete()
                return redirect('admin_list_conductor')
            except Driver.DoesNotExist():
                conductores = Driver.objects.all()
                return render(request, 'gooverWeb/admin_list_conductor.html', {'title': 'Lista de conductores',
                                                                               'mensaje': 'No se puede actualizar',
                                                                               'items' : conductores })
        else:
            return redirect('admin_list_conductor')
    return render(request, 'gooverWeb/inicio.html', {})


#########################################
def admin_list_cliente(request):
    if request.session.get('rol') == 'admin':
        clientes = Client.objects.all()
        return render(request, 'gooverWeb/admin_list_cliente.html', {'title': 'Lista de clientes','items' : clientes})
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

def admin_edit_cliente(request,id):
    if request.session.get('rol') == 'admin':
        post = get_object_or_404(Client, id=id)
        if request.method == "POST":
            form = ClientForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                try:
                    person_set = Client.objects.get(id=id)
                    person_set.name = post.name
                    person_set.last_name= post.last_name
                    person_set.phone = (post.phone)
                    person_set.password = (post.password)
                    person_set.photo = (post.photo)
                    person_set.email = post.email
                    person_set.save()
                    return redirect('admin_list_cliente')
                except Client.DoesNotExist():
                    items = Client.objects.all()
                    return render(request, 'gooverWeb/admin_list_cliente.html', {'title': 'Lista de Clientes',
                                                                                   'items' : items,
                                                                                   'mensaje': 'No se puede actualizar' })

        else:
            form = ClientForm(instance=post)
        return render(request, 'gooverWeb/admin_edit_cliente.html', {'form': form})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_delete_cliente(request,id):
    if request.session.get('rol') == 'admin':
        if request.method != "POST":
            try:
                person_set = Client.objects.get(id=id)
                person_set.delete()
                return redirect('admin_list_cliente')
            except Client.DoesNotExist():
                items = Client.objects.all()
                return render(request, 'gooverWeb/admin_list_cliente.html', {'title': 'Lista de conductores',
                                                                               'mensaje': 'No se puede actualizar',
                                                                               'items' : items })
        else:
            return redirect('admin_list_cliente')
    return render(request, 'gooverWeb/inicio.html', {})


#########################################
def admin_list_empleado(request):
    if request.session.get('rol') == 'admin':
        empleados = Employee.objects.all()
        return render(request, 'gooverWeb/admin_list_empleado.html', {'title': 'Lista de empleados','items' : empleados})
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

def admin_edit_employee(request,id):
    if request.session.get('rol') == 'admin':
        post = get_object_or_404(Employee, id=id)
        if request.method == "POST":
            form = EmployeeForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                try:
                    person_set = Employee.objects.get(id=id)
                    person_set.name = post.name
                    person_set.last_name= post.last_name
                    person_set.phone = (post.phone)
                    person_set.access_key = (post.access_key)
                    person_set.photo = (post.photo)
                    person_set.email = post.email
                    person_set.rol_id = post.rol_id
                    person_set.save()
                    return redirect('admin_list_empleado')
                except Employee.DoesNotExist():
                    items = Employee.objects.all()
                    return render(request, 'gooverWeb/admin_list_empleado.html', {'title': 'Lista de Empleados',
                                                                                   'items' : items,
                                                                                   'mensaje': 'No se puede actualizar informacion' })

        else:
            form = EmployeeForm(instance=post)
        return render(request, 'gooverWeb/admin_edit_employee.html', {'form': form})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_delete_empleado(request,id):
    if request.session.get('rol') == 'admin':
        if request.method != "POST":
            try:
                person_set = Employee.objects.get(id=id)
                person_set.delete()
                return redirect('admin_list_empleado')
            except Employee.DoesNotExist():
                items = Employee.objects.all()
                return render(request, 'gooverWeb/admin_list_empleado.html', {'title': 'Lista de Empleados',
                                                                               'mensaje': 'No se puede actualizar informacion',
                                                                               'items' : items })
        else:
            return redirect('admin_list_empleado')
    return render(request, 'gooverWeb/inicio.html', {})


####################################
def admin_list_reserva(request):
    if request.session.get('rol') == 'admin':
        reservas = Reservation.objects.all()
        return render(request, 'gooverWeb/admin_list_reserva.html', {'title': 'Lista de reservas','items' : reservas})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_edit_reserva(request,id):
    if request.session.get('rol') == 'admin':
        post = get_object_or_404(Reservation, id=id)
        if request.method == "POST":
            form = ReservaEditForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                try:
                    person_set = Reservation.objects.get(id=id)
                    person_set.reservation_hour = post.reservation_hour
                    person_set.reservation_date = post.reservation_date
                    person_set.longitude_ini = post.longitude_ini
                    person_set.latitude_ini = post.latitude_ini
                    person_set.longitude_fin = post.longitude_fin
                    person_set.latitude_fin = post.latitude_fin
                    person_set.price = post.price
                    person_set.payment_method = post.payment_method
                    person_set.client_id = post.client_id
                    person_set.conductor_id = post.conductor_id
                    person_set.status = post.status
                    person_set.save()
                    return redirect('admin_list_reserva')
                except Reservation.DoesNotExist():
                    reservas = Reservation.objects.all()
                    return render(request, 'gooverWeb/admin_list_reserva.html', {'title': 'Lista de reservas',
                                                                                 'items': reservas ,
                                                                                 'mensaje': 'No se puede actualizar'})

        else:
            form = ReservaEditForm(instance=post)
        return render(request, 'gooverWeb/admin_edit_reserva.html', {'form': form})
    return render(request, 'gooverWeb/inicio.html', {})

def admin_delete_reserva(request,id):
    if request.session.get('rol') == 'admin':
        if request.method != "POST":
            try:
                person_set = Reservation.objects.get(id=id)
                person_set.delete()
                return redirect('admin_list_reserva')
            except Reservation.DoesNotExist():
                return render(request, 'gooverWeb/admin_list_reserva.html', {'mensaje': 'No se puede actualizar' })
        else:
            return redirect('admin_list_reserva')
    return render(request, 'gooverWeb/inicio.html', {})

def admin_reserva(request):
    if request.session.get('rol') == 'admin':
        clientes = Client.objects.all()
        conductores = Driver.objects.all()
        if request.method == "POST":
            new_rol = ReservaForm(request.POST)
            if new_rol.is_valid():
                post = new_rol.save(commit=False)
                post.status = 'TO_BEGIN'
                post.save()
                return redirect('admin_dashboard')
            else:
                print(new_rol)
                return render(request, 'gooverWeb/admin_reserva.html', {'reserva': new_rol , 'mensaje': 'Verificar Informacion'})
        else:
            new_rol = ReservaForm()
        return render(request, 'gooverWeb/admin_reserva.html', {'reserva': new_rol ,
                                                                'clientes' : clientes ,
                                                                'conductores' : conductores})
    return render(request, 'gooverWeb/inicio.html', {})

###################################

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

