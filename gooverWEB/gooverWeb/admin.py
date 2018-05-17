from django.contrib import admin
from .models import Employee, Rol , Reservation

admin.site.register(Employee)
admin.site.register(Rol)

admin.site.register(Reservation)