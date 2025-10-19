from django.urls import path
from . import views

app_name = "recetas"

urlpatterns = [
    path("listar/", views.receta_list, name="list"),
    path("crear/", views.receta_create, name="create"),
    path("editar/<int:pk>/", views.receta_update, name="editar"),
    path("eliminar/<int:pk>/", views.receta_delete, name="eliminar"),
]
