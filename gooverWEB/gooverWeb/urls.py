from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.post_list),
    url('inicio', views.inicio, name='inicio'),
    url('login', views.login, name='login'),
    url('registro', views.registro, name='registro'),
    url('client_dashboard', views.client_dashboard, name='client_dashboard'),
]
