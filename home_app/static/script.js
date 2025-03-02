let batchChart; // Globální proměnná pro uchování instance grafu

function updateDesiredTemp(change) {
    fetch('/update_temp/', {
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

// Funkce pro načtení dat a vykreslení grafu pro aktuální senzor
async function fetchData() {
    const response = await fetch('/get_sensor_data/');
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return await response.json();
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

// Zavolejte renderChart() pro aktuální senzor
renderChart();

function toggleFermentation() {
    let button = document.getElementById("fermentButton");
    let fermentName = document.getElementById("ferment-name").value.trim();
    let isActive = button.innerText.includes("Deaktivovat");

    if (!isActive && !fermentName) {
        alert("Zadejte název fermentace!");
        return;
    }

    let formData = new FormData();
    if (!isActive) {
        formData.append("name", fermentName);
    }

    fetch(isActive ? "/stop_fermentation/" : "/start_fermentation/", {
        method: "POST",
        headers: {
            "X-CSRFToken": "{{ csrf_token }}" // Nezapomeňte na CSRF token
        },
        body: isActive ? null : formData // Pokud deaktivujeme, neposíláme nic
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            location.reload(); // Obnovíme stránku, aby se zobrazila správná data
        } else {
            alert("Chyba: " + data.message);
        }
    })
    .catch(error => console.error("Error:", error));
}

async function fetchBatchData(batchId) {
    console.log(`Načítání dat pro várku: ${batchId}`); // Debugging
    const response = await fetch(`/get_batch_data/${batchId}/`);
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    const data = await response.json();
    console.log(data); // Debugging
    return data;
}

async function renderBatchChart(batchId) {
    const data = await fetchBatchData(batchId);

    if (!data.labels.length || !data.temperature.length || !data.humidity.length) {
        console.error('Žádná data pro graf!');
        alert('Žádná data pro vybranou várku.');
        return; // Ukončete funkci, pokud jsou data prázdná
    }

    const ctx = document.getElementById('selectedBatchChart').getContext('2d');

    // Pokud graf již existuje, zničte ho před vykreslením nového
    if (batchChart) {
        batchChart.destroy();
    }

    batchChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels.reverse(),
            datasets: [
                {
                    label: 'Teplota (°C)',
                    data: data.temperature.reverse(),
                    borderColor: 'red',
                    fill: false
                },
                {
                    label: 'Vlhkost (%)',
                    data: data.humidity.reverse(),
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
    }); // Zde byla přidána závorka pro uzavření funkce renderBatchChart
}

function renderBatchChartForSelected() {
    const batchId = document.getElementById('batchSelect').value;
    if (batchId) {
        renderBatchChart(batchId);
    }
}


function deleteSelectedBatch() {
    const batchId = document.getElementById('batchSelect').value;
    if (!batchId) {
        alert("Vyberte várku, kterou chcete smazat!");
        return;
    }

    if (confirm("Opravdu chcete smazat tuto várku?")) {
        fetch(`/delete_batch/${batchId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',  // Zahrňte CSRF token
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert("Várka byla úspěšně smazána!");
                location.reload();  // Obnovte stránku nebo aktualizujte seznam
            } else {
                alert("Chyba při mazání várky: " + data.message);
            }
        })
        .catch(error => {
            console.error("Chyba:", error);
        });
    }
}
