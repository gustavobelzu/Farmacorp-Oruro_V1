from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, F
from datetime import datetime
import pandas as pd, io, matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from ventas.models import Venta, DetalleVenta
from farmacia.models import Sucursal
from .models import Reporte
from .forms import ReporteForm
import json


# =============================
# DASHBOARD PRINCIPAL
# =============================
def reporte_dashboard(request):
    """Dashboard general de reportes y estadísticas"""
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")
    sucursal_id = request.GET.get("sucursal")

    ventas = Venta.objects.all()
    if fecha_inicio and fecha_fin:
        ventas = ventas.filter(fecha__range=[fecha_inicio, fecha_fin])
    if sucursal_id:
        ventas = ventas.filter(sucursal_id=sucursal_id)

    total = ventas.aggregate(s=Sum("total"))["s"] or 0

    # Ventas por sucursal (para gráfico)
    data_grafico = (
        ventas.values("sucursal__nombre")
        .annotate(total=Sum("total"))
        .order_by("-total")
    )

    # Productos más vendidos
    top_productos = (
        DetalleVenta.objects
        .filter(venta__in=ventas)
        .values(nombre=F("producto__nombre"))
        .annotate(
            cantidad_total=Sum("cantidad"),
            total_vendido=Sum(F("cantidad") * F("precio_unitario"))
        )
        .order_by("-cantidad_total")[:10]
    )

    # === Calcular ganancias ===
    detalles = DetalleVenta.objects.filter(venta__in=ventas).select_related("producto")
    ingresos = detalles.aggregate(total=Sum(F("cantidad") * F("precio_unitario")))["total"] or 0
    costos = detalles.aggregate(total=Sum(F("cantidad") * F("producto__precio_unitario")))["total"] or 0
    ganancia = ingresos - costos

    # Convertir datos a JSON para los gráficos
    data_grafico_json = json.dumps(list(data_grafico), default=str)
    top_productos_json = json.dumps(list(top_productos), default=str)

    sucursales = Sucursal.objects.all()

    return render(request, "reportes/dashboard.html", {
        "ventas": ventas,
        "total": total,
        "data_grafico": data_grafico_json,
        "top_productos": top_productos_json,
        "sucursales": sucursales,
        "ingresos": ingresos,
        "costos": costos,
        "ganancia": ganancia,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
    })


# =============================
# CRUD DE REPORTES
# =============================
def reporte_list(request):
    reportes = Reporte.objects.all()
    return render(request, "reportes/list.html", {"reportes": reportes})


def reporte_create(request):
    form = ReporteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("reportes:list")
    return render(request, "reportes/form.html", {"form": form})


def reporte_update(request, pk):
    reporte = get_object_or_404(Reporte, pk=pk)
    form = ReporteForm(request.POST or None, instance=reporte)
    if form.is_valid():
        form.save()
        return redirect("reportes:list")
    return render(request, "reportes/form.html", {"form": form})


def reporte_delete(request, pk):
    reporte = get_object_or_404(Reporte, pk=pk)
    if request.method == "POST":
        reporte.delete()
        return redirect("reportes:list")
    return render(request, "reportes/delete.html", {"reporte": reporte})


# =============================
# EXPORTACIONES
# =============================
def ventas_filtradas(request):
    qs = Venta.objects.all()
    fi = request.GET.get('fecha_inicio')
    ff = request.GET.get('fecha_fin')
    if fi and ff:
        qs = qs.filter(fecha__date__range=[fi, ff])
    return qs


def exportar_excel(request):
    qs = ventas_filtradas(request)
    df = pd.DataFrame(list(qs.values('id_venta','fecha','total','sucursal__nombre','cliente__nombre')))
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='openpyxl') as writer:
        # Hoja 1: Ventas
        df.to_excel(writer, index=False, sheet_name='Ventas')

        # Hoja 2: Top Productos
        detalles = DetalleVenta.objects.filter(venta__in=qs).values(
            'producto__nombre'
        ).annotate(cantidad_total=Sum('cantidad')).order_by('-cantidad_total')[:10]
        df_top = pd.DataFrame(list(detalles))
        df_top.to_excel(writer, index=False, sheet_name='Top Productos')

        # 🧮 Hoja 3: Ganancias
        detalles_g = DetalleVenta.objects.filter(venta__in=qs).select_related("producto")
        ingresos = detalles_g.aggregate(total=Sum(F("cantidad") * F("precio_unitario")))["total"] or 0
        costos = detalles_g.aggregate(total=Sum(F("cantidad") * F("producto__costo_unitario")))["total"] or 0
        ganancia = ingresos - costos

        df_ganancia = pd.DataFrame([{
            "Ingresos (Bs)": ingresos,
            "Costos (Bs)": costos,
            "Ganancia Neta (Bs)": ganancia
        }])
        df_ganancia.to_excel(writer, index=False, sheet_name='Ganancias')

    out.seek(0)
    resp = HttpResponse(out.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    resp['Content-Disposition'] = 'attachment; filename=reporte_ventas.xlsx'
    return resp


def exportar_pdf(request):
    qs = ventas_filtradas(request)
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Reporte de Ventas", styles['Title']))
    elements.append(Spacer(1,12))

    # === Gráfico de Ventas por Sucursal ===
    df = pd.DataFrame(list(qs.values('sucursal__nombre','total')))
    if not df.empty:
        fig, ax = plt.subplots(figsize=(6,3))
        df.groupby('sucursal__nombre')['total'].sum().plot(kind='bar', ax=ax, color="#198754")
        ax.set_title('Ventas por Sucursal')
        ax.set_ylabel('Total (Bs)')
        imgbuf = io.BytesIO()
        plt.savefig(imgbuf, format='png', bbox_inches='tight')
        plt.close(fig)
        imgbuf.seek(0)
        elements.append(Image(imgbuf, width=480, height=240))
        elements.append(Spacer(1,12))

    # === Gráfico de Ganancias ===
    detalles = DetalleVenta.objects.filter(venta__in=qs).select_related("producto")
    ingresos = detalles.aggregate(total=Sum(F("cantidad") * F("precio_unitario")))["total"] or 0
    costos = detalles.aggregate(total=Sum(F("cantidad") * F("producto__costo_unitario")))["total"] or 0
    ganancia = ingresos - costos

    fig2, ax2 = plt.subplots(figsize=(4,3))
    ax2.bar(["Ingresos", "Costos", "Ganancia"], [ingresos, costos, ganancia],
             color=["#0d6efd","#c9a227","#198754"])
    ax2.set_title("Ingresos vs Costos vs Ganancia Neta")
    ax2.set_ylabel("Monto (Bs)")
    img_ganancia = io.BytesIO()
    plt.savefig(img_ganancia, format='png', bbox_inches='tight')
    plt.close(fig2)
    img_ganancia.seek(0)
    elements.append(Image(img_ganancia, width=400, height=220))
    elements.append(Spacer(1,12))

    elements.append(Paragraph(f"Total ventas: {qs.aggregate(sum=Sum('total'))['sum'] or 0:.2f}", styles['Normal']))
    elements.append(Paragraph(f"Generado: {datetime.now().strftime('%d-%m-%Y %H:%M')}", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return HttpResponse(buffer.read(), content_type='application/pdf', headers={'Content-Disposition':'attachment; filename=reporte_ventas.pdf'})


# =============================
# REPORTE DE GANANCIAS
# =============================
def reporte_ganancias(request):
    fi = request.GET.get("fecha_inicio")
    ff = request.GET.get("fecha_fin")
    sucursal_id = request.GET.get("sucursal")

    ventas = Venta.objects.all()
    if fi and ff:
        ventas = ventas.filter(fecha__range=[fi, ff])
    if sucursal_id:
        ventas = ventas.filter(sucursal_id=sucursal_id)

    detalles = DetalleVenta.objects.filter(venta__in=ventas).select_related("producto")

    ingresos = detalles.aggregate(total=Sum(F("cantidad") * F("precio_unitario")))["total"] or 0
    costos = detalles.aggregate(total=Sum(F("cantidad") * F("producto__precio_unitario")))["total"] or 0
    ganancia = ingresos - costos

    sucursales = Sucursal.objects.all()

    return render(request, "reportes/ganancias.html", {
        "fecha_inicio": fi,
        "fecha_fin": ff,
        "sucursal_id": sucursal_id,
        "sucursales": sucursales,
        "ingresos": ingresos,
        "costos": costos,
        "ganancia": ganancia,
    })
