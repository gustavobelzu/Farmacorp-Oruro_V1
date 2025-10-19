from django import forms
from .models import Inventario
from .models import Almacen

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = "__all__"

class AlmacenForm(forms.ModelForm):
    class Meta:
        model = Almacen
        fields = "__all__"
