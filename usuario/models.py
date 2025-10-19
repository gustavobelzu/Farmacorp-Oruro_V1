from django.contrib.auth.models import AbstractUser
from django.db import models
from empleados.models import Empleado
from clientes.models import Cliente

class Usuario(AbstractUser):
    ci_empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ci_cliente=models.OneToOneField(Cliente, on_delete=models.CASCADE, null=True, blank=True)

    def rol(self):
        if hasattr(self.ci_empleado, 'farmaceutico'):
            return 'farmaceutico'
        elif hasattr(self.ci_empleado, 'administrador'):
            return 'administrador'
        elif hasattr(self.ci_empleado, 'encargadoinventario'):
            return 'jefe_almacen'
        elif hasattr(self.ci_cliente,'cliente'):
            return 'cliente'
