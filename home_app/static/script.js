function updateDesiredTemp(change) {
    fetch('/api/update_temp/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ change: change }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            location.reload();
        } else {
            alert("Chyba při aktualizaci teploty: " + data.message);
        }
    })
    .catch(error => {
        console.error("Chyba:", error);
    });
}

// Funkce pro načtení dat a vykreslení grafu
async function fetchData() {
    const response = await fetch('/get_sensor_data/');  // Změněno na správnou URL
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    const data = await response.json();
    return data;
}

async function renderChart() {
    try {
        const data = await fetchData();

        // Obrácení pořadí dat, aby nejnovější hodnoty byly vpravo
        data.labels.reverse();
        data.temperature.reverse();
        data.humidity.reverse();

        const ctx = document.getElementById('sensorChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Teplota (°C)',
                        data: data.temperature,
                        borderColor: 'red',
                        fill: false
                    },
                    {
                        label: 'Vlhkost (%)',
                        data: data.humidity,
                        borderColor: 'blue',
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    x: { title: { display: true, text: 'Čas' } },
                    y: { title: { display: true, text: 'Hodnota' } }
                }
            }
        });
    } catch (error) {
        console.error("Chyba při vykreslování grafu:", error);
    }
}

renderChart();

function toggleFermentation() {
    let button = document.getElementById("fermentButton");
    let fermentName = document.getElementById("ferment-name").value.trim();
    let isActive = button.innerText.includes("Deaktivovat");

    if (!isActive && !fermentName) {
        alert("Zadejte název fermentace!");
        return;
    }

    fetch(isActive ? "/stop_fermentation/" : "/start_fermentation/", {
        method: "POST",
        headers: {
            "X-CSRFToken": "{{ csrf_token }}",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(isActive ? {} : { name: fermentName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            button.innerText = isActive ? "Aktivovat fermentaci" : "Deaktivovat fermentaci";
        } else {
            alert("Chyba: " + data.message);
        }
    })
    .catch(error => console.error("Error:", error));
}
