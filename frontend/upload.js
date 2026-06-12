const API_BASE = "http://localhost:8000/api/v1";
let uploadedFileName = "";
let currentContactData = null;
let duplicateContactId = null;

// Setup drag and drop
const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");

uploadArea.addEventListener("click", () => fileInput.click());

uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadArea.classList.add("dragover");
});

uploadArea.addEventListener("dragleave", () => {
    uploadArea.classList.remove("dragover");
});

uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadArea.classList.remove("dragover");
    handleFiles(e.dataTransfer.files);
});

fileInput.addEventListener("change", (e) => {
    handleFiles(e.target.files);
});

function handleFiles(files) {
    if (files.length === 0) return;
    
    const file = files[0];
    uploadFile(file);
}

async function uploadFile(file) {
    // Validate file
    const validTypes = ["image/jpeg", "image/png", "image/jpg", "application/pdf"];
    if (!validTypes.includes(file.type)) {
        showError("Please select a valid image file (JPG, PNG, or PDF)");
        return;
    }
    
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
        showError("File size exceeds 10MB limit");
        return;
    }
    
    // Show processing section
    showProcessing();
    
    try {
        const formData = new FormData();
        formData.append("file", file);
        uploadedFileName = file.name;
        
        const response = await fetch(`${API_BASE}/visiting-card/upload`, {
            method: "POST",
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Upload failed");
        }
        
        const result = await response.json();
        
        if (result.status === "duplicate") {
            showDuplicate(result);
        } else if (result.status === "success") {
            showExtractedData(result);
        }
    } catch (error) {
        console.error("Error uploading file:", error);
        showError(error.message || "Failed to process image");
        resetForm();
    }
}

function showProcessing() {
    document.querySelector(".upload-section").style.display = "none";
    document.getElementById("processingSection").style.display = "block";
    document.getElementById("duplicateSection").style.display = "none";
    document.getElementById("successSection").style.display = "none";
}

function showExtractedData(result) {
    const extracted = result.extracted_data;
    currentContactData = extracted;
    
    // Display preview image
    const previewImg = document.getElementById("previewImage");
    if (extracted.image_path) {
        previewImg.src = extracted.image_path;
    }
    
    // Fill form
    document.getElementById("name").value = extracted.name || "";
    document.getElementById("designation").value = extracted.designation || "";
    document.getElementById("company_name").value = extracted.company_name || "";
    document.getElementById("mobile").value = extracted.mobile || "";
    document.getElementById("email").value = extracted.email || "";
    document.getElementById("website").value = extracted.website || "";
    document.getElementById("address").value = extracted.address || "";
    document.getElementById("confidence").value = extracted.ocr_confidence;
    document.getElementById("rawTextContent").textContent = extracted.raw_text;
    
    // Show form with extracted data
    document.querySelector(".extracted-data").style.display = "block";
    document.getElementById("rawOCRText").style.display = "block";
}

function showDuplicate(result) {
    const extracted = result.extracted_data;
    currentContactData = extracted;
    duplicateContactId = result.existing_id;
    
    document.getElementById("processingSection").style.display = "none";
    document.getElementById("duplicateSection").style.display = "block";
    
    // Show new card info
    const newInfo = document.getElementById("newContactInfo");
    newInfo.innerHTML = `
        <p><strong>Name:</strong> ${extracted.name || "N/A"}</p>
        <p><strong>Designation:</strong> ${extracted.designation || "N/A"}</p>
        <p><strong>Company:</strong> ${extracted.company_name || "N/A"}</p>
        <p><strong>Email:</strong> ${extracted.email || "N/A"}</p>
        <p><strong>Mobile:</strong> ${extracted.mobile || "N/A"}</p>
        <p><strong>OCR Confidence:</strong> ${extracted.ocr_confidence}</p>
    `;
    
    // You could fetch and display existing contact info here
}

document.getElementById("extractedForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
        return;
    }
    
    // Form is already filled and contact was created on upload
    // Just show success
    showSuccess(result.contact_id);
});

function validateForm() {
    let isValid = true;
    
    const name = document.getElementById("name").value.trim();
    if (!name) {
        showFieldError("nameError", "Name is required");
        isValid = false;
    } else {
        clearFieldError("nameError");
    }
    
    const email = document.getElementById("email").value.trim();
    if (email && !isValidEmail(email)) {
        showFieldError("emailError", "Invalid email format");
        isValid = false;
    } else {
        clearFieldError("emailError");
    }
    
    const mobile = document.getElementById("mobile").value.trim();
    if (mobile && !isValidPhone(mobile)) {
        showFieldError("mobileError", "Invalid phone format");
        isValid = false;
    } else {
        clearFieldError("mobileError");
    }
    
    return isValid;
}

function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function isValidPhone(phone) {
    const re = /^[\d\s+\-()]{10,}$/;
    return re.test(phone);
}

function showFieldError(fieldId, message) {
    document.getElementById(fieldId).textContent = message;
}

function clearFieldError(fieldId) {
    document.getElementById(fieldId).textContent = "";
}

function showSuccess(contactId) {
    document.getElementById("processingSection").style.display = "none";
    document.getElementById("duplicateSection").style.display = "none";
    document.getElementById("successSection").style.display = "block";
    document.getElementById("successMessage").textContent = 
        `Contact has been successfully added to the database. Contact ID: ${contactId}`;
}

function showError(message) {
    alert("Error: " + message);
}

function cancelUpload() {
    resetForm();
}

function resetForm() {
    document.querySelector(".upload-section").style.display = "block";
    document.getElementById("processingSection").style.display = "none";
    document.getElementById("duplicateSection").style.display = "none";
    document.getElementById("successSection").style.display = "none";
    
    fileInput.value = "";
    document.getElementById("extractedForm").reset();
    currentContactData = null;
    duplicateContactId = null;
}

function saveDuplicate() {
    // In a real app, this would create a new contact anyway or merge
    showSuccess(duplicateContactId);
}

function goToDashboard() {
    window.location.href = "index.html";
}

function uploadAnother() {
    resetForm();
}
