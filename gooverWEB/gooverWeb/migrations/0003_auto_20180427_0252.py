# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-27 08:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gooverWeb', '0002_auto_20180427_0251'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('phone', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('password', models.CharField(max_length=32)),
                ('virtual_cash', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('photo_license', models.ImageField(blank=True, null=True, upload_to='')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField()),
                ('access_key', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField()),
                ('access_key', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='MarcaVehiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ModeloVehiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_hour', models.DateTimeField()),
                ('reservation_date', models.DateField()),
                ('longitude_ini', models.DecimalField(decimal_places=10, max_digits=12)),
                ('latitude_ini', models.DecimalField(decimal_places=10, max_digits=12)),
                ('longitude_fin', models.DecimalField(decimal_places=10, max_digits=12)),
                ('latitude_fin', models.DecimalField(decimal_places=10, max_digits=12)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('CASH', 'EFECTIVO'), ('CREDIT_CARD', 'TARJETA_CREDITO'), ('VIRTUAL_CASH', 'MONEDA_VIRTUAL')], default='CASH', max_length=10)),
                ('year_in_school', models.CharField(choices=[('TO_BEGIN', 'POR_INICIAR'), ('IN_PROCESS', 'EN_PROCESO'), ('COMPLETE', 'COMPLETADA'), ('CANCELED', 'CANCELADA')], default='TO_BEGIN', max_length=10)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gooverWeb.Client')),
                ('conductor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gooverWeb.Driver')),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=1900)),
                ('photo', models.ImageField(upload_to='')),
                ('license_plate', models.CharField(max_length=200)),
                ('color', models.CharField(max_length=200)),
                ('conductor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gooverWeb.Driver')),
                ('marca_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gooverWeb.MarcaVehiculo')),
                ('modelo_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gooverWeb.ModeloVehiculo')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='rol_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gooverWeb.Rol'),
        ),
        migrations.AddField(
            model_name='driver',
            name='rol_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gooverWeb.Rol'),
        ),
    ]