from django.urls import path
from . import views

app_name = "inventario"

urlpatterns = [
    path("", views.InventarioListView.as_view(), name="list"),
    path("crear/", views.inventario_create, name="create"),
    path("editar/<int:pk>/", views.inventario_update, name="update"),
    path("eliminar/<int:pk>/", views.inventario_delete, name="delete"),

    # CRUD de Almacén
    path("almacenes/", views.almacen_list, name="almacen_list"),
    path("almacenes/crear/", views.almacen_create, name="almacen_create"),
    path("almacenes/editar/<int:pk>/", views.almacen_update, name="almacen_update"),
    path("almacenes/eliminar/<int:pk>/", views.almacen_delete, name="almacen_delete"),

    # API para actualizar stock
    path("api/actualizar_stock/", views.actualizar_stock, name="api_actualizar_stock"),
]


