from django.shortcuts import render, get_object_or_404, redirect
from datetime import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UsuarioCreateForm
from django.contrib.auth.decorators import user_passes_test
from ventas.models import Venta
from clientes.models import Cliente
from productos.models import Producto
from alertas.models import Alerta
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ventas.models import Venta
from clientes.models import Cliente
from productos.models import Producto
from alertas.models import Alerta
from django.contrib import messages
from .models import Usuario

def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST, request=request)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("usuario:dashboard")
    else:
        form = LoginForm()
    return render(request, "usuario/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")

def registrar_usuario(request):
    form = UsuarioCreateForm(request.POST or None)
    if form.is_valid():
        usuario = form.save(commit=False)

        # Asignar rol según relación
        if usuario.ci_empleado:
            usuario.username = f"emp_{usuario.ci_empleado.ci}"
        elif usuario.ci_cliente:
            usuario.username = f"cli_{usuario.ci_cliente.ci}"

        usuario.save()
        login(request, usuario)
        messages.success(request, "Usuario registrado correctamente.")
        return redirect("usuario:dashboard")  # Redirige según tu estructura

    return render(request, "usuario/register.html", {"form": form})

def registrar_usuario(request):
    form = UsuarioCreateForm(request.POST or None)
    if form.is_valid():
        usuario = form.save(commit=False)

        # Asignar rol según relación
        if usuario.ci_empleado:
            usuario.username = f"emp_{usuario.ci_empleado.ci}"
        elif usuario.ci_cliente:
            usuario.username = f"cli_{usuario.ci_cliente.ci}"

        usuario.save()
        login(request, usuario)
        messages.success(request, "Usuario registrado correctamente.")
        return redirect("usuario:dashboard")  # Redirige según tu estructura

    return render(request, "usuario/register.html", {"form": form})

def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == "POST":
        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect("usuarios:list")
    return render(request, "usuario/delete.html", {"usuario": usuario})

def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    form = UsuarioCreateForm(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        messages.success(request, "Usuario actualizado correctamente.")
        return redirect("usuarios:list")  # o al dashboard
    return render(request, "usuario/form.html", {"form": form})

def usuario_list(request):
    usuarios = Usuario.objects.select_related("ci_empleado", "ci_cliente").order_by("-fecha_creacion")
    return render(request, "usuario/list.html", {"usuarios": usuarios})



@login_required
def dashboard(request):
    user = request.user
    rol = getattr(user, "rol", None)

    #Si es cliente, redirige directamente a su historial
    if rol == "cliente":
        return redirect("Cliente:historial")

    # Panel general según rol
    context = {"user": user, "rol": rol}

    if rol == "administrador":
        context.update({
            "total_ventas": Venta.objects.count(),
            "total_clientes": Cliente.objects.count(),
            "total_productos": Producto.objects.count(),
            "total_alertas": Alerta.objects.filter(estado=True).count(),
        })

    elif rol == "farmaceutico":
        # Datos específicos del farmacéutico
        context.update({
            "ventas_dia": Venta.objects.filter(fecha__date=timezone.now().date()).count(),
            "alertas": Alerta.objects.filter(estado=True).order_by("-fecha_alerta")[:5],
        })

    elif rol == "jefe_almacen":
        # Datos del almacén
        context.update({
            "productos_bajos": Producto.objects.filter(stock__lte=5),
            "alertas_stock": Alerta.objects.filter(tipo="Stock Bajo"),
        })

    return render(request, "usuario/dashboard.html", context)
