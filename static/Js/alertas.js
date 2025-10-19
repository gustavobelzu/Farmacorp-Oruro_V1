document.addEventListener("DOMContentLoaded", () => {
  const alertCount = document.getElementById("alertCount");
  const alertList = document.getElementById("alertList");

  function cargarAlertas() {
    fetch("/alertas/api/") // ← asegúrate que la URL coincida con tu ruta
      .then(res => res.json())
      .then(data => {
        const count = data.count;
        const alertas = data.alertas;

        // Actualiza contador
        if (count > 0) {
          alertCount.textContent = count;
          alertCount.classList.remove("d-none");
        } else {
          alertCount.classList.add("d-none");
        }

        // Construye el menú de alertas
        alertList.innerHTML = `
          <li class="dropdown-header text-center fw-bold text-danger">Alertas Recientes</li>
          <li><hr class="dropdown-divider"></li>
          ${alertas.map(a => `
            <li class="px-3 py-2">
              <strong class="text-danger">${a.tipo}</strong><br>
              <small>${a.descripcion}</small><br>
              <span class="text-muted small">${a.producto}</span>
            </li>
          `).join("")}
          <li><hr class="dropdown-divider"></li>
          <li class="text-center">
            <a href="/alertas/" class="text-success fw-bold">Ver todas</a>
          </li>
        `;
      })
      .catch(err => console.error("Error cargando alertas:", err));
  }

  // Carga inicial
  cargarAlertas();

  // Refresca cada 60 segundos
  setInterval(cargarAlertas, 60000);
});
