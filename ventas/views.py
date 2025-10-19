from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import Sum
from django.contrib import messages
from decimal import Decimal
import json
from .models import Venta, DetalleVenta
from .forms import VentaForm
from productos.models import Producto
from clientes.models import Cliente
from empleados.models import Empleado
from farmacia.models import Sucursal

# ========================================================
# FUNCIONES AUXILIARES
# ========================================================

def calcular_subtotal(cantidad, precio_unitario, descuento=0, iva=0):
    """Calcula subtotal con descuento e IVA"""
    bruto = cantidad * precio_unitario
    descuento_val = bruto * (descuento / 100)
    iva_val = (bruto - descuento_val) * (iva / 100)
    return bruto - descuento_val + iva_val


# ========================================================
# CRUD DE VENTAS
# ========================================================

@login_required
def venta_list(request):
    """Lista todas las ventas registradas"""
    ventas = Venta.objects.select_related("cliente", "empleado", "sucursal")
    return render(request, "ventas/list.html", {"ventas": ventas})


@login_required
def venta_update(request, pk):
    """Editar una venta"""
    venta = get_object_or_404(Venta, pk=pk)
    form = VentaForm(request.POST or None, instance=venta)
    if form.is_valid():
        form.save()
        messages.success(request, "Venta actualizada correctamente.")
        return redirect("ventas:list")
    return render(request, "ventas/form.html", {"form": form})


@login_required
def venta_delete(request, pk):
    """Eliminar una venta"""
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == "POST":
        venta.delete()
        messages.success(request, "Venta eliminada correctamente.")
        return redirect("ventas:list")
    return render(request, "ventas/delete.html", {"venta": venta})


# ========================================================
# POS Y CREACIÓN DE VENTAS
# ========================================================

@login_required
def pos(request):
    """Vista principal del punto de venta"""
    productos = Producto.objects.all()
    clientes = Cliente.objects.all()
    empleados = Empleado.objects.all()
    sucursales = Sucursal.objects.all()
    return render(request, "ventas/venta_pos.html", {
        "productos": productos,
        "clientes": clientes,
        "empleados": empleados,
        "sucursales": sucursales
    })


@login_required
@transaction.atomic
def crear_venta(request):
    if request.method == "POST":
        try:
            cliente_id = request.POST.get("cliente")
            empleado_id = request.POST.get("empleado")
            sucursal_id = request.POST.get("sucursal")

            cliente = get_object_or_404(Cliente, pk=cliente_id)
            empleado = get_object_or_404(Empleado, pk=empleado_id)
            sucursal = get_object_or_404(Sucursal, pk=sucursal_id)

            venta = Venta.objects.create(
                cliente=cliente,
                empleado=empleado,
                sucursal=sucursal,
                total=0
            )

            total = Decimal(0)
            productos = request.POST.getlist("producto")
            cantidades = request.POST.getlist("cantidad")
            descuentos = request.POST.getlist("descuento")
            metodos = request.POST.getlist("metodo_pago")  # nuevo campo

            for i in range(len(productos)):
                codigo = productos[i]
                cantidad = int(cantidades[i])
                descuento = Decimal(descuentos[i] or 0)
                metodo = metodos[i] if i < len(metodos) else "efectivo"

                prod = Producto.objects.get(codigo_barras=codigo)
                precio = prod.precio_unitario
                subtotal = precio * cantidad * (1 - descuento / 100)

                DetalleVenta.objects.create(
                    venta=venta,
                    producto=prod,
                    cantidad=cantidad,
                    descuento=descuento,
                    precio_unitario=precio,
                    subtotal=subtotal,
                    metodo_pago=metodo
                )

                total += subtotal

            venta.total = total
            venta.estado = "pagado"  # si el pago es inmediato
            venta.save()

            messages.success(request, f"Venta #{venta.pk} registrada correctamente.")
            return redirect("ventas:detalle", pk=venta.pk)

        except Exception as e:
            messages.error(request, f"Error al registrar la venta: {e}")
            return redirect("ventas:venta_pos")

    return redirect("ventas:venta_pos")



# ========================================================
# API - VERIFICACIÓN DE TOTAL
# ========================================================

@csrf_exempt
def api_verificar_total(request):
    """
    Verifica el total calculado desde el cliente.
    Espera JSON con formato:
    {
      "items": [
        {"codigo": "123", "cantidad": 2, "descuento": 10}
      ]
    }
    """
    try:
        data = json.loads(request.body)
        items = data.get("items", [])
        total = Decimal(0)

        for it in items:
            prod = Producto.objects.get(codigo_barras=it["codigo"])
            qty = Decimal(it["cantidad"])
            descuento = Decimal(it.get("descuento", 0))
            subtotal = prod.precio_unitario * qty * (1 - descuento / 100)
            total += subtotal

        return JsonResponse({"ok": True, "total": str(total)})

    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=400)


# ========================================================
# DETALLE DE VENTA Y PAGOS
# ========================================================

@login_required
def detalle_venta(request, pk):
    """Muestra el detalle completo de una venta"""
    venta = get_object_or_404(Venta, pk=pk)
    detalles = venta.detalles.all()
    return render(request, "ventas/detalle.html", {
        "venta": venta,
        "detalles": detalles
    })



# ========================================================
# RECIBO Y VALIDACIÓN
# ========================================================

class ReciboExtendidoView(DetailView):
    model = Venta
    template_name = 'ventas/recibo_extendido.html'
    context_object_name = 'venta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = self.object.detalles.all()
        context['total'] = sum(d.subtotal for d in context['detalles'])
        return context


@login_required
def validar_venta(request, venta_id):
    """Valida que el total calculado coincida con el registrado"""
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)
    total_calculado = sum(d.cantidad * d.precio_unitario for d in detalles)
    return render(request, "ventas/recibo_extendido.html", {
        "venta": venta,
        "detalles": detalles,
        "total_calculado": total_calculado
    })
