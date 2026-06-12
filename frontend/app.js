const API_BASE = "http://localhost:8000/api/v1";
let currentPage = 1;
const pageSize = 10;

// Helper function to convert file paths to URLs
function getImageUrl(imagePath) {
    if (!imagePath) return "";
    if (imagePath.startsWith("/uploads/")) return imagePath;
    if (imagePath.includes("backend/uploads/")) {
        return "/uploads/" + imagePath.split("/").pop();
    }
    return imagePath;
}

// Load contacts on page load
document.addEventListener("DOMContentLoaded", () => {
    loadContacts();
});

async function loadContacts(page = 1) {
    try {
        const skip = (page - 1) * pageSize;
        const response = await fetch(
            `${API_BASE}/contacts?skip=${skip}&limit=${pageSize}`
        );
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const contacts = await response.json();
        displayContacts(contacts);
        currentPage = page;
        updatePagination(contacts.length);
    } catch (error) {
        console.error("Error loading contacts:", error);
        displayError("Failed to load contacts");
    }
}

function displayContacts(contacts) {
    const tbody = document.getElementById("contactsTableBody");
    
    if (contacts.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="no-data">No contacts found</td></tr>';
        document.getElementById("totalContacts").textContent = "0";
        return;
    }

    tbody.innerHTML = contacts.map(contact => `
        <tr>
            <td>${contact.name || "N/A"}</td>
            <td>${contact.designation || "N/A"}</td>
            <td>${contact.company_name || "N/A"}</td>
            <td>${contact.email || "N/A"}</td>
            <td>${contact.mobile || "N/A"}</td>
            <td>
                <button class="btn-action" onclick="viewContact(${contact.id})">View</button>
                <button class="btn-action btn-danger" onclick="deleteContact(${contact.id})">Delete</button>
            </td>
        </tr>
    `).join("");
    
    document.getElementById("totalContacts").textContent = contacts.length;
}

async function viewContact(contactId) {
    try {
        const response = await fetch(`${API_BASE}/contact/${contactId}`);
        
        if (!response.ok) {
            throw new Error("Failed to fetch contact");
        }
        
        const contact = await response.json();
        displayContactModal(contact);
    } catch (error) {
        console.error("Error loading contact:", error);
        displayError("Failed to load contact details");
    }
}

function displayContactModal(contact) {
    const modal = document.getElementById("contactModal");
    const details = document.getElementById("contactDetails");
    
    const createdDate = new Date(contact.created_at).toLocaleDateString();
    
    details.innerHTML = `
        <h2>${contact.name}</h2>
        <div class="modal-body">
            <div class="detail-group">
                <label>Name:</label>
                <span>${contact.name}</span>
            </div>
            <div class="detail-group">
                <label>Designation:</label>
                <span>${contact.designation || "N/A"}</span>
            </div>
            <div class="detail-group">
                <label>Company:</label>
                <span>${contact.company_name || "N/A"}</span>
            </div>
            <div class="detail-group">
                <label>Email:</label>
                <span>${contact.email || "N/A"}</span>
            </div>
            <div class="detail-group">
                <label>Mobile:</label>
                <span>${contact.mobile || "N/A"}</span>
            </div>
            <div class="detail-group">
                <label>Website:</label>
                <span>${contact.website || "N/A"}</span>
            </div>
            <div class="detail-group">
                <label>Address:</label>
                <span>${contact.address || "N/A"}</span>
            </div>
            <div class="detail-group">
                <label>OCR Confidence:</label>
                <span>${contact.confidence_score}%</span>
            </div>
            <div class="detail-group">
                <label>Added:</label>
                <span>${createdDate}</span>
            </div>
            ${contact.image_path ? `
                <div class="detail-group">
                    <label>Card Image:</label>
                    <img src="${getImageUrl(contact.image_path)}" alt="Visiting Card" class="contact-image">
                </div>
            ` : ""}
            <div class="modal-actions">
                <button class="btn btn-primary" onclick="editContact(${contact.id})">Edit</button>
                <button class="btn btn-secondary" onclick="closeModal()">Close</button>
            </div>
        </div>
    `;
    
    modal.style.display = "block";
}

function closeModal() {
    document.getElementById("contactModal").style.display = "none";
}

async function deleteContact(contactId) {
    if (!confirm("Are you sure you want to delete this contact?")) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/contact/${contactId}`, {
            method: "DELETE"
        });
        
        if (!response.ok) {
            throw new Error("Failed to delete contact");
        }
        
        loadContacts(currentPage);
        displaySuccess("Contact deleted successfully");
    } catch (error) {
        console.error("Error deleting contact:", error);
        displayError("Failed to delete contact");
    }
}

async function searchContacts() {
    const query = document.getElementById("searchInput").value.trim();
    
    if (!query) {
        displayError("Please enter a search term");
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/contacts/search?q=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error("Search failed");
        }
        
        const contacts = await response.json();
        displayContacts(contacts);
        document.getElementById("pageInfo").textContent = `Search results for: "${query}"`;
    } catch (error) {
        console.error("Error searching:", error);
        displayError("Search failed");
    }
}

function resetSearch() {
    document.getElementById("searchInput").value = "";
    loadContacts(1);
}

function updatePagination(contactCount) {
    document.getElementById("pageInfo").textContent = `Page ${currentPage}`;
}

function previousPage() {
    if (currentPage > 1) {
        loadContacts(currentPage - 1);
    }
}

function nextPage() {
    loadContacts(currentPage + 1);
}

function editContact(contactId) {
    // Redirect to edit page (would need to implement)
    alert("Edit functionality would be implemented here");
}

function displayError(message) {
    alert(message);
}

function displaySuccess(message) {
    alert(message);
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById("contactModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
}
