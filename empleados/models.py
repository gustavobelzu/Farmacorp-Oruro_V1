from django.db import models

from farmacia.models import Sucursal

class Empleado(models.Model):
    CARGOS = [
        ("farmaceutico", "Farmacéutico"),
        ("administrador", "Administrador"),
        ("inventario", "Encargado de Inventario"),
    ]
    ci = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    cargo = models.CharField(max_length=20, choices=CARGOS)
    sexo = models.CharField(max_length=10)
    estado = models.BooleanField(default=True)
    turno = models.CharField(max_length=50)
    sucursal=models.ForeignKey(Sucursal,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"
def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    if self.cargo == "farmaceutico":
        Farmaceutico.objects.get_or_create(empleado=self)
    elif self.cargo == "administrador":
        Administrador.objects.get_or_create(empleado=self)
    elif self.cargo == "inventario":
        EncargadoInventario.objects.get_or_create(empleado=self)


class Farmaceutico(models.Model):
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE, primary_key=True)
    matricula = models.CharField(max_length=50)
    especialidad = models.CharField(max_length=100)


class Administrador(models.Model):
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE, primary_key=True)


class EncargadoInventario(models.Model):
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE, primary_key=True)
