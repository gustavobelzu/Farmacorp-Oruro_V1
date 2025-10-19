from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from .models import Cliente
from .forms import ClienteForm
from ventas.models import Venta


#  Listar todos los clientes
@login_required
def cliente_list(request):
    clientes = Cliente.objects.all().order_by("nombre")
    return render(request, "clientes/list.html", {"clientes": clientes})


#  Crear un cliente
@login_required
def cliente_create(request):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("clientes:list")
    return render(request, "clientes/form.html", {"form": form})


#  Editar un cliente
@login_required
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        return redirect("clientes:list")
    return render(request, "clientes/form.html", {"form": form})


#  Eliminar un cliente
@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.delete()
        return redirect("clientes:list")
    return render(request, "clientes/delete.html", {"cliente": cliente})


#  Ver historial de compras y recetas de un cliente
@login_required
def historial_cliente(request, ci_cliente):
    cliente = get_object_or_404(Cliente, ci_cliente=ci_cliente)
    ventas = cliente.ventas.select_related("sucursal", "empleado").order_by("-fecha")
    recetas = cliente.recetas.select_related("empleado").order_by("-fecha_emision")

    total_gastado = ventas.aggregate(total=Sum("total"))["total"] or 0

    return render(request, "clientes/historial.html", {
        "cliente": cliente,
        "ventas": ventas,
        "recetas": recetas,
        "total_gastado": total_gastado
    })


# API: Clientes con más compras (para dashboard o reportes)
@login_required
def api_clientes_top(request):
    """
    Devuelve los clientes que más han comprado (para usar con Chart.js u otros gráficos)
    """
    data = (
        Venta.objects.values("cliente__nombre")
        .annotate(total_gastado=Sum("total"))
        .order_by("-total_gastado")[:5]
    )

    labels = [d["cliente__nombre"] for d in data]
    values = [float(d["total_gastado"]) for d in data]

    return JsonResponse({"labels": labels, "values": values})
