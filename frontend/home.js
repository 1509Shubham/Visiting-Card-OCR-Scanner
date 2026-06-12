const API_BASE = "http://localhost:8000";

// Check API status on page load
document.addEventListener("DOMContentLoaded", () => {
    checkAPIStatus();
    checkDatabaseStatus();
    loadContactsCount();
});

async function checkAPIStatus() {
    try {
        const response = await fetch(`${API_BASE}/`);
        if (response.ok) {
            updateStatus("apiStatus", true, "Connected");
        } else {
            updateStatus("apiStatus", false, "Error");
        }
    } catch (error) {
        updateStatus("apiStatus", false, "Offline");
    }
}

async function checkDatabaseStatus() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        if (data.status === "healthy") {
            updateStatus("dbStatus", true, "Connected");
        } else {
            updateStatus("dbStatus", false, "Disconnected");
        }
    } catch (error) {
        updateStatus("dbStatus", false, "Offline");
    }
}

async function loadContactsCount() {
    try {
        const response = await fetch(`${API_BASE}/api/v1/contacts?limit=1`);
        const data = await response.json();
        // Get total count from headers if available, otherwise show 0
        const count = data.length > 0 ? data.length : 0;
        document.querySelector("#contactsCount .status-number").textContent = count;
    } catch (error) {
        console.error("Error loading contacts count:", error);
    }
}

function updateStatus(elementId, isOnline, text) {
    const element = document.getElementById(elementId);
    const icon = element.querySelector(".status-icon");
    const statusText = element.querySelector(".status-text");
    
    if (isOnline) {
        icon.classList.remove("loading");
        icon.classList.add("online");
        icon.textContent = "✓";
    } else {
        icon.classList.remove("loading");
        icon.classList.add("offline");
        icon.textContent = "✗";
    }
    
    statusText.textContent = text;
}
