from django.db import models
from farmacia.models import Sucursal

class Reporte(models.Model):
    id_Reporte=models.AutoField(primary_key=True)
    Fecha_Reporte=models.DateField()
    Tipo=models.CharField(max_length=50)
    Sucursal=models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="reportes")
