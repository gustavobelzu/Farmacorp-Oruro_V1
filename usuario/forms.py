from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Usuario
from empleados.models import Empleado
from clientes.models import Cliente

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

class UsuarioCreateForm(UserCreationForm):
    ci_empleado = forms.ModelChoiceField(queryset=Empleado.objects.all(), required=False)
    ci_cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False)

    class Meta:
        model = Usuario
        fields = ["username", "email", "password1", "password2", "ci_empleado", "ci_cliente"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

