from django.urls import path
from . import views

app_name = "farmacia"

urlpatterns = [
    # Farmacia
    path("farmacias/", views.farmacia_list, name="list"),
    path("farmacias/nueva/", views.farmacia_create, name="create"),
    path("farmacias/<int:pk>/editar/", views.farmacia_update, name="farmacia_update"),
    path("farmacias/<int:pk>/eliminar/", views.farmacia_delete, name="farmacia_delete"),

    # Sucursal
    path("sucursales/", views.sucursal_list, name="listf"),
    path("sucursales/nueva/", views.sucursal_create, name="sucursal_create"),
    path("sucursales/<int:pk>/editar/", views.sucursal_update, name="sucursal_update"),
    path("sucursales/<int:pk>/eliminar/", views.sucursal_delete, name="sucursal_delete"),
]
