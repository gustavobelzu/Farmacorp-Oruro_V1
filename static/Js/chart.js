// chart.js - Dashboard de Farmacorp
document.addEventListener("DOMContentLoaded", () => {
    // === Elementos del DOM ===
    const ventasChartCanvas = document.getElementById("ventasChart");
    const productosChartCanvas = document.getElementById("productosChart");
    const clientesChartCanvas = document.getElementById("clientesChart");
    const gananciasChartCanvas = document.getElementById("gananciasChart");

    // === Paleta de colores institucional ===
    const colors = {
        verde: "#198754",
        verdeOscuro: "#146c43",
        dorado: "#c9a227",
        azul: "#0d6efd",
        celeste: "#20c997",
        naranja: "#fd7e14",
        grisClaro: "#f8f9fa"
    };

    // ===========================================
    // 📊 GRÁFICO: Ventas por Sucursal
    // ===========================================
    if (ventasChartCanvas) {
        try {
            const ctx = ventasChartCanvas.getContext("2d");
            const rawData = ventasChartCanvas.dataset.grafico || "[]";
            const data = JSON.parse(rawData);

            const labels = data.map(d => d.sucursal__nombre);
            const valores = data.map(d => parseFloat(d.total));

            new Chart(ctx, {
                type: "bar",
                data: {
                    labels,
                    datasets: [{
                        label: "Ventas por Sucursal (Bs)",
                        data: valores,
                        backgroundColor: colors.verde,
                        borderColor: colors.verdeOscuro,
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: { display: true, text: "Total (Bs)" }
                        }
                    },
                    plugins: {
                        legend: { display: false },
                        title: { display: true, text: "Ventas por Sucursal" }
                    }
                }
            });
        } catch (error) {
            console.error("❌ Error al renderizar gráfico de ventas:", error);
        }
    }

    // ===========================================
    // 💰 GRÁFICO: Ingresos vs Costos vs Ganancia
    // ===========================================
    if (gananciasChartCanvas) {
        try {
            const ctx = gananciasChartCanvas.getContext("2d");
            const ingresos = parseFloat(gananciasChartCanvas.dataset.ingresos || "0");
            const costos = parseFloat(gananciasChartCanvas.dataset.costos || "0");
            const ganancia = parseFloat(gananciasChartCanvas.dataset.ganancia || "0");

            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: ["Ingresos", "Costos", "Ganancia Neta"],
                    datasets: [{
                        label: "Monto (Bs)",
                        data: [ingresos, costos, ganancia],
                        backgroundColor: [colors.azul, colors.dorado, colors.verde],
                        borderColor: [colors.azul, colors.naranja, colors.verdeOscuro],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: { display: true, text: "Monto (Bs)" }
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: "Ingresos vs Costos vs Ganancia"
                        },
                        legend: { display: false }
                    }
                }
            });
        } catch (error) {
            console.error("❌ Error al renderizar gráfico de ganancias:", error);
        }
    }

    // ===========================================
    // 💊 GRÁFICO: Productos más vendidos
    // (se obtiene dinámicamente desde API Django)
    // ===========================================
    if (productosChartCanvas) {
        fetch("/reportes/api/productos_mas_vendidos/")
            .then(res => {
                if (!res.ok) throw new Error(`Error HTTP ${res.status}`);
                return res.json();
            })
            .then(data => {
                const ctx = productosChartCanvas.getContext("2d");
                new Chart(ctx, {
                    type: "pie",
                    data: {
                        labels: data.labels,
                        datasets: [{
                            data: data.values,
                            backgroundColor: [
                                colors.verde,
                                colors.dorado,
                                colors.azul,
                                colors.celeste,
                                colors.naranja
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            title: {
                                display: true,
                                text: "Productos Más Vendidos"
                            },
                            legend: {
                                position: "bottom"
                            }
                        }
                    }
                });
            })
            .catch(err => console.error("❌ Error cargando productos:", err));
    }

    // ===========================================
    // 🧍‍♂️ GRÁFICO: Clientes con más compras
    // ===========================================
    if (clientesChartCanvas) {
        fetch("/clientes/api/top_clientes/")
            .then(res => {
                if (!res.ok) throw new Error(`Error HTTP ${res.status}`);
                return res.json();
            })
            .then(data => {
                const ctx = clientesChartCanvas.getContext("2d");
                new Chart(ctx, {
                    type: "bar",
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: "Compras Totales (Bs)",
                            data: data.values,
                            backgroundColor: colors.celeste,
                            borderColor: colors.azul,
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: { y: { beginAtZero: true } },
                        plugins: {
                            title: {
                                display: true,
                                text: "Top 5 Clientes"
                            },
                            legend: { display: false }
                        }
                    }
                });
            })
            .catch(err => console.error("❌ Error cargando clientes:", err));
    }
});
