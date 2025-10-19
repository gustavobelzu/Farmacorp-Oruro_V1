from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Proveedor,Compra
from .forms import ProductoForm, ProveedorForm,CompraForm
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib import messages
from inventario.models import Inventario

#crud de productos
@login_required
def producto_list(request):
    productos = Producto.objects.all()
    return render(request, "productos/list.html", {"productos": productos})

@login_required
def producto_create(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos:list")
    else:
        form = ProductoForm()
    return render(request, "productos/form.html", {"form": form})

@login_required
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("productos:list")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "productos/form.html", {"form": form})

@login_required
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    return redirect("productos:list")

#crud de proveedores
def proveedor_list(request):
    proveedores = Proveedor.objects.all()
    return render(request, "proveedores/listp.html", {"proveedores": proveedores})

def proveedor_create(request):
    form = ProveedorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("proveedores:listp")
    return render(request, "proveedores/form.html", {"form": form})

def proveedor_update(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    form = ProveedorForm(request.POST or None, instance=proveedor)
    if form.is_valid():
        form.save()
        return redirect("proveedores:listp")
    return render(request, "proveedores/form.html", {"form": form})

def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == "POST":
        proveedor.delete()
        return redirect("proveedores:listp")
    return render(request, "proveedores/delete.html", {"proveedor": proveedor})
 #Requerimiento f8
 
class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/detalle.html'
    context_object_name = 'producto'
    pk_url_kwarg = 'codigo_barras'


def producto_detail(request, codigo):
    producto = get_object_or_404(Producto, codigo_barras=codigo)
    # sustitutos: productos con nombre similar o campo generico si existe
    sustitutos = Producto.objects.filter(nombre__icontains=producto.nombre.split()[0]).exclude(pk=producto.pk)[:5]
    return render(request, 'productos/detail.html', {'producto':producto, 'sustitutos':sustitutos})
# Compra CRUD
def compra_list(request):
    compras = Compra.objects.select_related("producto")
    return render(request, "compras/listc.html", {"compras": compras})

def compra_create(request):
    form = CompraForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Compra registrada correctamente.")
        return redirect("compras:listc")
    return render(request, "compras/form.html", {"form": form})

def compra_update(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    form = CompraForm(request.POST or None, instance=compra)
    if form.is_valid():
        form.save()
        messages.success(request, "Compra actualizada correctamente.")
        return redirect("compras:listc")
    return render(request, "compras/form.html", {"form": form})

def compra_delete(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    if request.method == "POST":
        compra.delete()
        messages.success(request, "Compra eliminada correctamente.")
        return redirect("compras:listc")
    return render(request, "compras/delete.html", {"compra": compra})
