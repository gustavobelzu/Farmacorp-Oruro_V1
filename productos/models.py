from django.db import models
import json

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.TextField()
    estado = models.BooleanField(default=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    codigo_barras = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)
    fecha_vencimiento = models.DateField()
    iva = models.DecimalField(max_digits=5, decimal_places=2)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name="productos")

    def __str__(self):
        return self.nombre
    
    
class Compra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="compras")
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    fecha_compra = models.DateField(auto_now_add=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.producto.stock += self.cantidad
        self.producto.precio_unitario = self.precio_compra//self.cantidad
        self.producto.save()
    

    def __str__(self):
        return f"Compra de {self.producto.nombre} - {self.cantidad} unidades"

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ["-fecha_compra"]
