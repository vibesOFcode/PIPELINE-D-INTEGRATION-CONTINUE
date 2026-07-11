// Récupérer les variables CSS
const rootStyles = getComputedStyle(document.documentElement);
const colorText = rootStyles.getPropertyValue("--text").trim();
const colorBlue = rootStyles.getPropertyValue("--blue").trim();
const colorYellow = rootStyles.getPropertyValue("--yellow").trim();
const colorRed = rootStyles.getPropertyValue("--red").trim();
const colorGrid = rootStyles.getPropertyValue("--overlay0").trim();

let chart;
let currentPeriod = 'hour';

function setPeriod(period) {
  currentPeriod = period;
  // Re-draw chart if data available
  if (window.currentStats) {
    updateChart(window.currentStats);
  }
}

async function sendFile() {
  const fileInput = document.getElementById("fileInput");
  if (!fileInput.files.length) return;

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const response = await fetch("http://localhost:8000/stats", {
      method: "POST",
      body: formData,
    });
    if (!response.ok) throw new Error("Network issue: " + response.status);
    const stats = await response.json();

    if (stats.error) {
      alert("Error: " + stats.error);
      return;
    }

    window.currentStats = stats;

    // --- Update Table ---
    const tbody = document.querySelector("#resultTable tbody");
    tbody.innerHTML = "";
    for (const key of ["LINES", "INFO", "WARN", "ERROR", "unique_ips"]) {
      const row = document.createElement("tr");
      const typeCell = document.createElement("td");
      typeCell.textContent = key;
      const valueCell = document.createElement("td");
      valueCell.textContent = stats[key];
      row.appendChild(typeCell);
      row.appendChild(valueCell);
      tbody.appendChild(row);
    }

    // --- Update Top IPs ---
    const ipTbody = document.querySelector("#topIpTable tbody");
    ipTbody.innerHTML = "";
    if (stats.top_ips.length > 0) {
      stats.top_ips.forEach(([ip, count]) => {
        const row = document.createElement("tr");
        const ipCell = document.createElement("td");
        ipCell.textContent = ip;
        const countCell = document.createElement("td");
        countCell.textContent = count;
        row.appendChild(ipCell);
        row.appendChild(countCell);
        ipTbody.appendChild(row);
      });
    } else {
      const row = document.createElement("tr");
      const cell = document.createElement("td");
      cell.colSpan = 2;
      cell.textContent = "No IPs";
      row.appendChild(cell);
      ipTbody.appendChild(row);
    }

    // --- Update Last Errors ---
    const ul = document.getElementById("lastErrors");
    ul.innerHTML = "";
    if (stats.last_errors.length > 0) {
      stats.last_errors.forEach(error => {
        const li = document.createElement("li");
        li.textContent = error;
        ul.appendChild(li);
      });
    } else {
      const li = document.createElement("li");
      li.textContent = "No errors";
      ul.appendChild(li);
    }

    // --- Update Chart ---
    updateChart(stats);

  } catch (err) {
    alert("Error : " + err);
  }
}

function updateChart(stats) {
  const ctx = document.getElementById("statsChart").getContext("2d");
  const histoKey = `error_histogram_${currentPeriod}`;
  const histo = stats[histoKey] || {};
  const labels = Object.keys(histo).sort();
  const data = labels.map(label => histo[label]);

  const chartData = {
    labels: labels,
    datasets: [
      {
        label: `Errors per ${currentPeriod}`,
        data: data,
        backgroundColor: colorRed + "CC",
        borderColor: colorRed,
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: false, labels: { color: colorText } },
      title: {
        display: true,
        text: `Error Histogram (${currentPeriod})`,
        color: colorText,
      },
    },
    scales: {
      x: { ticks: { color: colorText }, grid: { color: colorGrid } },
      y: { ticks: { color: colorText }, grid: { color: colorGrid } },
    },
  };

  if (chart) {
    chart.data = chartData;
    chart.options = options;
    chart.update();
  } else {
    chart = new Chart(ctx, { type: "line", data: chartData, options });
  }
}
