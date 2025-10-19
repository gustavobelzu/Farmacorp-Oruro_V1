from django import forms
from .models import Farmacia, Sucursal

class FarmaciaForm(forms.ModelForm):
    class Meta:
        model = Farmacia
        fields = "__all__"


class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ["nombre", "departamento", "nit", "email", "direccion", "horario", "farmacia"]
