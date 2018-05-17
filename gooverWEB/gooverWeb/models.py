from django.db import models


class ModeloVehiculo(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

    def setName(self, name):
        self.nombre = name

    def getName(self):
        return self.nombre


class MarcaVehiculo(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

    def setName(self, name):
        self.nombre = name

    def getName(self):
        return self.nombre


class Rol(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

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
    photo = models.ImageField(upload_to='tmp',blank=True, null=True)
    email = models.EmailField()
    phone = models.IntegerField()
    access_key = models.CharField(max_length=8)
    rol_id = models.ForeignKey(Rol)

    def __str__(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def getLast_Name(self):
        return  self.last_name

    def setLast_Name(self,last_name):
        self.last_name = last_name

    def getPhone(self):
        return  self.phone

    def setPhone(self,phone):
        self.phone = phone

    def getEmail(self):
        return self.email

    def setEmail(self,email):
        self.email = email

    def getPhoto(self):
        return self.photo

    def setPhoto(self, photo):
        self.photo = photo

    def getAccesKey(self):
        return  self.access_key

    def setAccessKey(self,access_key):
        self.access_key = access_key

    def getRol(self):
        return self.rol_id

    def setRol(self, rol_id):
        self.rol_id = rol_id


class Driver(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='tmp',blank=True, null=True)
    photo_license = models.ImageField(upload_to='tmp',blank=True, null=True)
    email = models.EmailField()
    phone = models.IntegerField()
    access_key = models.CharField(max_length=8)
    rol_id = models.ForeignKey(Rol)

    def __str__(self):
        return '%s %s <%s>' % (self.name,self.last_name,self.email)

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
    photo = models.ImageField(upload_to='tmp', blank=True, null=True)
    password = models.CharField(max_length=32)
    virtual_cash = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return  '%s %s <%s>' % (self.name,self.last_name,self.email)

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def getLast_Name(self):
        return  self.last_name

    def setLast_Name(self,last_name):
        self.last_name = last_name

    def getPhone(self):
        return  self.phone

    def setPhone(self,phone):
        self.phone = phone

    def getEmail(self):
        return self.email

    def setEmail(self,email):
        self.email = email

    def getPhoto(self):
        return self.photo

    def setPhoto(self, photo):
        self.photo = photo

    def getPassword(self):
        return  self.password

    def setPassword(self,password):
        self.password = password

    def getVirtual_Cash(self):
        return  self.virtual_cash

    def setVirtual_Cash(self,virtual_cash):
        self.virtual_cash = virtual_cash


class Reservation(models.Model):
    client_id = models.ForeignKey(Client)
    conductor_id = models.ForeignKey(Driver)
    reservation_hour = models.TimeField()
    reservation_date = models.DateField()
    longitude_ini = models.DecimalField(max_digits=12, decimal_places=10)
    latitude_ini = models.DecimalField(max_digits=12, decimal_places=10)
    longitude_fin = models.DecimalField(max_digits=12, decimal_places=10)
    latitude_fin = models.DecimalField(max_digits=12, decimal_places=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    PAYMENT_CHOICES = (
        ('CASH', 'EFECTIVO'),
        ('CARD', 'TARJETA_CREDITO'),
        ('VIRTUAL', 'MONEDA_VIRTUAL')
    )
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='CASH')
    STATUS_CHOICES = (
        ('TO_BEGIN', 'POR_INICIAR'),
        ('IN_PROCESS', 'EN_PROCESO'),
        ('COMPLETE', 'COMPLETADA'),
        ('CANCELED', 'CANCELADA'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='TO_BEGIN')
