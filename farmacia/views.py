from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Farmacia, Sucursal
from .forms import FarmaciaForm, SucursalForm

# -------- FARMACIA --------
@login_required
def farmacia_list(request):
    farmacias = Farmacia.objects.all()
    return render(request, "farmacia/list.html", {"farmacias": farmacias})

@login_required
def farmacia_create(request):
    if request.method == "POST":
        form = FarmaciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("farmacia:farmacia_list")
    else:
        form = FarmaciaForm()
    return render(request, "farmacia/form.html", {"form": form})

@login_required
def farmacia_update(request, pk):
    farmacia = get_object_or_404(Farmacia, pk=pk)
    if request.method == "POST":
        form = FarmaciaForm(request.POST, instance=farmacia)
        if form.is_valid():
            form.save()
            return redirect("farmacia:farmacia_list")
    else:
        form = FarmaciaForm(instance=farmacia)
    return render(request, "farmacia/form.html", {"form": form})

@login_required
def farmacia_delete(request, pk):
    farmacia = get_object_or_404(Farmacia, pk=pk)
    farmacia.delete()
    return redirect("farmacia:farmacia_list")

# -------- SUCURSAL --------
@login_required
def sucursal_list(request):
    sucursales = Sucursal.objects.all()
    return render(request, "sucursal/listf.html", {"sucursales": sucursales})

@login_required
def sucursal_create(request):
    if request.method == "POST":
        form = SucursalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sucursal:sucursal_list")
    else:
        form = SucursalForm()
    return render(request, "sucursal/form.html", {"form": form})

@login_required
def sucursal_update(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == "POST":
        form = SucursalForm(request.POST, instance=sucursal)
        if form.is_valid():
            form.save()
            return redirect("sucursal:sucursal_list")
    else:
        form = SucursalForm(instance=sucursal)
    return render(request, "sucursal/form.html", {"form": form})

@login_required
def sucursal_delete(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    sucursal.delete()
    return redirect("sucursal:sucursal_list")
