async function startTracking() {
    const uniqueId = document.getElementById("unique_id").value;
    if (!uniqueId) {
        alert("Inserisci un Unique ID!");
        return;
    }

    const response = await fetch(`/api/start-tracking?unique_id=${uniqueId}`);
    const data = await response.json();

    if (data.success) {
        updateResults(data);
        setInterval(() => fetchStatus(uniqueId), 60000); // Aggiorna ogni minuto
    } else {
        alert("Errore nell'avvio del tracking.");
    }
}

async function fetchStatus(uniqueId) {
    const response = await fetch(`/api/status?unique_id=${uniqueId}`);
    const data = await response.json();
    updateResults(data);
}

function updateResults(data) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = `
        <div class="card">
            <img src="${data.profile_pic}" alt="Profile">
            <h3>${data.unique_id}</h3>
            <button onclick="viewLive('${data.unique_id}')">Visualizza</button>
            <button onclick="downloadData('${data.unique_id}')">Scarica</button>
        </div>
    `;
}

function viewLive(uniqueId) {
    window.open(`/view/${uniqueId}`, "_blank");
}

function downloadData(uniqueId) {
    window.location.href = `/api/download?unique_id=${uniqueId}`;
}