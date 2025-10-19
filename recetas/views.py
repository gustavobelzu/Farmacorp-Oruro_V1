from django.shortcuts import render, redirect, get_object_or_404
from .models import Receta
from .forms import RecetaForm

def receta_list(request):
    recetas = Receta.objects.all()
    return render(request, "recetas/list.html", {"recetas": recetas})

def receta_create(request):
    form = RecetaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("recetas:list")
    return render(request, "recetas/form.html", {"form": form})

def receta_update(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    form = RecetaForm(request.POST or None, instance=receta)
    if form.is_valid():
        form.save()
        return redirect("recetas:list")
    return render(request, "recetas/form.html", {"form": form})

def receta_delete(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    if request.method == "POST":
        receta.delete()
        return redirect("recetas:list")
    return render(request, "recetas/delete.html", {"receta": receta})
