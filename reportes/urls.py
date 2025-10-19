from django.urls import path
from . import views

app_name = "reportes"

urlpatterns = [
    path('', views.reporte_list, name="list"),
    path("crear/", views.reporte_create, name="crear"),
    path("editar/<int:pk>/", views.reporte_update, name="editar"),
    path("eliminar/<int:pk>/", views.reporte_delete, name="eliminar"),
    path('exportar/excel/', views.exportar_excel, name='exportar_excel'),
    path('exportar/pdf/', views.exportar_pdf, name='exportar_pdf'),
    path("Dashboard/", views.reporte_dashboard, name="Dashboard"),
    path('ganancias/', views.reporte_ganancias, name='ganancias'),


]
