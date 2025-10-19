from django.db import models
from clientes.models import Cliente
from empleados.models import Empleado
from productos.models import Producto
from farmacia.models import Sucursal
from django.db.models import Sum, F
from decimal import Decimal


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    factura = models.BooleanField(default=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="ventas")
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name="ventas")
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="ventas")
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, default="pendiente")

    def save(self, *args, **kwargs):
        # Calcular subtotal con descuento
        bruto = self.precio_unitario * self.cantidad
        descuento_val = bruto * (self.descuento / 100)
        neto = bruto - descuento_val
        iva_val = neto * (self.iva / 100)
        self.subtotal = neto + iva_val
        # Obtener precio de compra actual
        ultima_compra = self.producto.compras.order_by("-fecha_compra").first()
        precio_compra = ultima_compra.precio_compra if ultima_compra else Decimal(0)
        # Calcular ganancia
        self.ganancia = (self.precio_unitario - precio_compra) * self.cantidad
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Venta {self.id_venta} - Total: {self.total}"
    def calcular_ganancia(self):
        return self.detalles.aggregate(
        total=Sum("ganancia")
        )["total"] or Decimal(0)



class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="detalles_ventas")
    cantidad = models.IntegerField()
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    metodo_pago = models.CharField(
        max_length=50,
        choices=[
            ("efectivo", "Efectivo"),
            ("tarjeta", "Tarjeta"),
            ("transferencia", "Transferencia"),
        ],
        default="efectivo")
    ganancia = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def save(self, *args, **kwargs):
        self.subtotal = (self.precio_unitario * self.cantidad) * (1 - (self.descuento or 0) / 100)
    # Obtener precio de compra actual
        ultima_compra = self.producto.compras.order_by("-fecha_compra").first()
        precio_compra = ultima_compra.precio_compra if ultima_compra else Decimal(0)
        self.ganancia = (self.precio_unitario - precio_compra) * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle de {self.venta} - {self.producto}"