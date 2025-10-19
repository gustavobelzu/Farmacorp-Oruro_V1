from django.db import models

class Farmacia(models.Model):
    id_farmacia = models.AutoField(primary_key=True)
    nombre_farmacia = models.CharField(max_length=150)
    razon_legal = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.nombre_farmacia


class Sucursal(models.Model):
    id_sucursal = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    DEPARTAMENTOS = [
    ("Oruro", "Oruro"),
    ("La Paz", "La Paz"),
    ("Cochabamba", "Cochabamba"),
    ("Potosi","Potosi"),
    ("Chuqisaca","Chuquisaca"),
    ("Pando","Pando"),
    ("Beni","Beni"),
    ("Santa Cruz","Santa Cruz"),
    ("Tarija","Tarija"),
]
    departamento = models.CharField(max_length=100, choices=DEPARTAMENTOS)
    nit = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    direccion = models.CharField(max_length=200)
    horario = models.CharField(max_length=100)
    fecha_registroSucursal = models.DateField(auto_now_add=True)
    # Relacion con Farmacia
    farmacia = models.ForeignKey(Farmacia, on_delete=models.CASCADE, related_name="sucursales")

    def __str__(self):
        return f"{self.nombre} - {self.departamento}"
