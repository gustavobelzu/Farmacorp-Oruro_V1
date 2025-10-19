from django.db import models
from farmacia.models import Sucursal
from productos.models import Producto
from utils.stock import actualizar_stock_producto

class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    estado = models.BooleanField(default=True)
    fecha_actualizacion = models.DateField(auto_now=True)
    stock_minimo = models.IntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} ({self.sucursal.nombre})"
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        actualizar_stock_producto(self.producto)

class Almacen(models.Model):
    id_almacen = models.AutoField(primary_key=True)
    Categoria = models.CharField(max_length=100)
    Ubicacion = models.CharField(max_length=200)
    Fecha_Ingreso=models.DateField(auto_now_add=True)
    Fecha_Salida=models.DateField(null=True, blank=True)
    id_Inventario=models.ForeignKey(Inventario, on_delete=models.CASCADE)

    
    def __str__(self):
        return f"{self.categoria} - {self.ubicacion}"