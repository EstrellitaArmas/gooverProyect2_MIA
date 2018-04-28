from django.db import models


class ModeloVehiculo(models.Model):
    nombre = models.CharField(max_length=200)

    def setName(self, name):
        self.nombre = name

    def getName(self):
        return self.nombre


class MarcaVehiculo(models.Model):
    nombre = models.CharField(max_length=200)

    def setName(self, name):
        self.nombre = name

    def getName(self):
        return self.nombre


class Rol(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setDescription(self, description):
        self.description = description

    def getDescription(self):
        return  self.description


class Employee(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    photo = models.ImageField(blank=True, null=True)
    email = models.EmailField()
    phone = models.IntegerField()
    access_key = models.CharField(max_length=8)
    rol_id = models.ForeignKey(Rol)

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def __str__(self):
        return self.name


class Driver(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    photo = models.ImageField(blank=True, null=True)
    photo_license = models.ImageField(blank=True, null=True)
    email = models.EmailField()
    phone = models.IntegerField()
    access_key = models.CharField(max_length=8)
    rol_id = models.ForeignKey(Rol)


class Vehiculo(models.Model):
    year = models.IntegerField(default=1900)
    photo = models.ImageField()
    license_plate = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    conductor_id = models.ForeignKey(Driver)
    marca_id = models.ForeignKey(MarcaVehiculo, models.SET_NULL, blank=True, null=True)
    modelo_id = models.ForeignKey(ModeloVehiculo, models.SET_NULL, blank=True, null=True)


class Client(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.IntegerField()
    email = models.EmailField()
    photo = models.ImageField(blank=True, null=True)
    password = models.CharField(max_length=32)
    virtual_cash = models.DecimalField(max_digits=10, decimal_places=2)


class Reservation(models.Model):
    client_id = models.ForeignKey(Client)
    conductor_id = models.ForeignKey(Driver)
    reservation_hour = models.DateTimeField()
    reservation_date = models.DateField()
    longitude_ini = models.DecimalField(max_digits=12, decimal_places=10)
    latitude_ini = models.DecimalField(max_digits=12, decimal_places=10)
    longitude_fin = models.DecimalField(max_digits=12, decimal_places=10)
    latitude_fin = models.DecimalField(max_digits=12, decimal_places=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    PAYMENT_CHOICES = (
        ('CASH', 'EFECTIVO'),
        ('CREDIT_CARD', 'TARJETA_CREDITO'),
        ('VIRTUAL_CASH', 'MONEDA_VIRTUAL')
    )
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='CASH')
    STATUS_CHOICES = (
        ('TO_BEGIN', 'POR_INICIAR'),
        ('IN_PROCESS', 'EN_PROCESO'),
        ('COMPLETE', 'COMPLETADA'),
        ('CANCELED', 'CANCELADA'),
    )
    year_in_school = models.CharField(max_length=10, choices=STATUS_CHOICES, default='TO_BEGIN')
