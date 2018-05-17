from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.post_list),
    url('inicio', views.inicio, name='inicio'),
    url('login', views.login, name='login'),
    url('registro', views.registro, name='registro'),
    url('client_dashboard', views.client_dashboard, name='client_dashboard'),
    url('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),


    url('admin_rol', views.admin_rol, name='admin_rol'),
    url('admin_list_rol', views.admin_list_rol, name='admin_list_rol'),
    url('admin_edit_rol/(?P<id>[0-9]+)/', views.admin_edit_rol, name='admin_edit_rol'),
    url('admin_delete_rol/(?P<id>[0-9]+)/', views.admin_delete_rol, name='admin_delete_rol'),

    url('admin_marca', views.admin_marca, name='admin_marca'),
    url('admin_modelo', views.admin_modelo, name='admin_modelo'),
    url('admin_vehiculo', views.admin_vehiculo, name='admin_vehiculo'),

    url('admin_list_marca', views.admin_list_marca, name='admin_list_marca'),
    url('admin_list_modelo', views.admin_list_modelo, name='admin_list_modelo'),
    url('admin_list_vehiculo', views.admin_list_vehiculo, name='admin_list_vehiculo'),

    url('admin_list_conductor', views.admin_list_conductor, name='admin_list_conductor'),
    url('admin_conductor', views.admin_conductor, name='admin_conductor'),
    url('admin_edit_conductor/(?P<id>[0-9]+)/', views.admin_edit_conductor, name='admin_edit_conductor'),
    url('admin_delete_conductor/(?P<id>[0-9]+)/', views.admin_delete_conductor, name='admin_delete_conductor'),

    url('admin_list_cliente', views.admin_list_cliente, name='admin_list_cliente'),
    url('admin_cliente', views.admin_cliente, name='admin_cliente'),
    url('admin_edit_cliente/(?P<id>[0-9]+)/', views.admin_edit_cliente, name='admin_edit_cliente'),
    url('admin_delete_cliente/(?P<id>[0-9]+)/', views.admin_delete_cliente, name='admin_delete_cliente'),

    url('admin_list_empleado', views.admin_list_empleado, name='admin_list_empleado'),
    url('admin_employee', views.admin_employee, name='admin_employee'),
    url('admin_edit_employee/(?P<id>[0-9]+)/', views.admin_edit_employee, name='admin_edit_employee'),
    url('admin_delete_empleado/(?P<id>[0-9]+)/', views.admin_delete_empleado, name='admin_delete_empleado'),

    url('admin_reserva', views.admin_reserva, name='admin_reserva'),
    url('admin_list_reserva', views.admin_list_reserva, name='admin_list_reserva'),
    url('admin_edit_reserva/(?P<id>[0-9]+)/', views.admin_edit_reserva, name='admin_edit_reserva'),
    url('admin_delete_reserva/(?P<id>[0-9]+)/', views.admin_delete_reserva, name='admin_delete_reserva'),

    url('admin_settings', views.admin_settings, name='admin_settings'),
    url('client_settings', views.client_settings, name='client_settings'),
    url('call_dashboard', views.admin_dashboard, name='call_dashboard'),
]
