from django import forms
from .models import Venta,DetalleVenta

class VentaForm(forms.ModelForm):
    class meta:
        model = Venta
        fields = '__all__'  

class DetalleVentaForm(forms.ModelForm):
    class meta:
        model=DetalleVenta
        fields='__all__'



