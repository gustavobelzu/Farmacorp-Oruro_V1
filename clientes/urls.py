from django.urls import path
from . import views

app_name = "clientes"

urlpatterns = [
    path("", views.cliente_list, name="list"),
    path("crear/", views.cliente_create, name="create"),
    path("editar/<int:pk>/", views.cliente_update, name="update"),
    path("eliminar/<int:pk>/", views.cliente_delete, name="delete"),
    path("historial/<str:ci_cliente>/", views.historial_cliente, name="historial"),
    
    # API para los clientes con más compras
    path("api/top_clientes/", views.api_clientes_top, name="api_top_clientes"),
]


