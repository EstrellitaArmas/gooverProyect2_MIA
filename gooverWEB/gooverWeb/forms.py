from django import forms
from .models import Client
from .models import Rol
from .models import Employee
from .models import MarcaVehiculo
from .models import ModeloVehiculo
from .models import Vehiculo
from .models import Driver
from .models import Reservation


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('email', 'name', 'last_name', 'password', 'phone', 'photo')


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('email', 'name', 'last_name', 'access_key', 'phone', 'photo', 'rol_id' )
        choice = forms.ModelMultipleChoiceField(queryset= Rol.objects.all())

class LoginForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('email', 'password')


class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ('name', 'description')


class MarcaForm(forms.ModelForm):
    class Meta:
        model = MarcaVehiculo
        fields = ('nombre',)

class ModeloForm(forms.ModelForm):
    class Meta:
        model = ModeloVehiculo
        fields = ('nombre',)

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ('license_plate', 'year', 'color', 'marca_id', 'modelo_id', 'conductor_id'  )
        choiceMarca = forms.ModelMultipleChoiceField(queryset= MarcaVehiculo.objects.all())
        choiceModelo = forms.ModelMultipleChoiceField(queryset=ModeloVehiculo.objects.all())
        choiceConductor = forms.ModelMultipleChoiceField(queryset=Driver.objects.all())

class ConductorForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ('name', 'last_name', 'access_key', 'phone', 'email', 'photo', 'photo_license', 'rol_id' )
        choice = forms.ModelMultipleChoiceField(queryset= Rol.objects.all())

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('reservation_date',
                  'longitude_ini','latitude_ini',
                  'longitude_fin', 'latitude_fin',
                  'price',
                  'client_id','conductor_id')
        choiceModelo = forms.ModelMultipleChoiceField(queryset=Client.objects.all())
        choiceConductor = forms.ModelMultipleChoiceField(queryset=Driver.objects.all())
