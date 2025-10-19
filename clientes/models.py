from django.db import models

class Cliente(models.Model):
    ci_cliente = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nombre} ({self.ci_cliente})"
