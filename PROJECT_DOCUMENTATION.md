# Visiting Card OCR Scanner - Complete Documentation

## Project Overview
A full-stack OCR-based system for scanning visiting cards, extracting structured information, and managing contact data with duplicate detection and web-based UI.

---

## Interview Questions & Answers

### Architecture & Design
**Q1: Explain the overall architecture of this project.**
A: The project follows a 3-tier architecture:
- **Frontend Layer**: HTML/CSS/JavaScript with responsive UI (home.html, upload.html, index.html)
- **API Layer**: FastAPI REST API with 7 endpoints for CRUD operations and OCR processing
- **Backend Layer**: SQLite database with SQLAlchemy ORM, OCR service using EasyOCR, entity extraction using regex

**Q2: What design patterns did you use?**
A: 
- **Service Layer Pattern**: OCRService, ContactService for business logic separation
- **Repository Pattern**: ContactService handles database operations
- **Dependency Injection**: FastAPI's Depends() for session management
- **MVC Pattern**: Routes (controllers), Schemas (models), Services (business logic)

**Q3: How do you handle scalability?**
A:
- Pagination support (skip/limit) in GET /contacts
- Lazy loading of OCR Reader (single instance)
- Static file caching via CDN-ready paths
- Database indexing on frequent queries (email, mobile)

---

### Frontend Development
**Q4: How does the frontend handle image uploads?**
A:
- Drag-and-drop file handler using HTML5 File API
- Client-side validation (file type: jpg/png/pdf, size: 10MB max)
- FormData API for multipart file uploads
- Preview image before submission
- Error handling with user-friendly messages

**Q5: Explain the state management in upload.js.**
A:
- Global variables: `uploadedFileName`, `result` for tracking upload state
- Form shows/hides based on operation status (processing, success, duplicate)
- localStorage NOT used - state resets on page refresh (stateless design)
- Modal overlays for duplicate detection UI

**Q6: How do you display contacts in the dashboard?**
A:
- Pagination: 10 contacts per page with Next/Previous buttons
- Table layout with columns: Name, Designation, Company, Email, Mobile, Actions
- View button opens modal with full details and card image
- Search functionality with real-time filtering
- Delete button with confirmation

**Q7: How do you handle CORS?**
A: Configured in FastAPI's CORSMiddleware with:
```python
allow_origins=["*"]
allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]
```
Allows frontend at any origin to access API endpoints.

---

### Backend API
**Q8: Describe the 7 API endpoints.**
A:
1. **POST /api/v1/visiting-card/upload**: Upload card image, extract text, detect duplicates, create contact
2. **GET /api/v1/contacts**: List all contacts with pagination (skip, limit)
3. **GET /api/v1/contact/{id}**: Retrieve single contact by ID
4. **PUT /api/v1/contact/{id}**: Update contact fields (partial updates)
5. **DELETE /api/v1/contact/{id}**: Delete contact by ID
6. **GET /api/v1/contacts/search**: Full-text search by name/email/mobile
7. **GET /health**: Health check endpoint (API + Database status)

**Q9: What is the upload flow?**
A:
1. Receive multipart file upload
2. Save file to `backend/uploads/` with timestamp prefix
3. Validate image format (jpg/png/pdf)
4. Extract text using EasyOCR
5. Extract entities (name, email, mobile, etc.) using regex
6. Check for duplicates by email or mobile
7. If duplicate exists → return existing contact ID
8. If new → create contact, return success with contact_id

**Q10: How do you handle duplicates?**
A:
- After OCR extraction, query database for matching email or mobile
- If found, return status="duplicate" with existing_id
- Frontend shows comparison UI: existing contact vs extracted data
- User can choose to ignore or update

**Q11: Explain error handling.**
A:
- HTTPException for known errors (400, 404, 500)
- Try-catch blocks with logging
- File cleanup on failure (remove uploaded file if OCR fails)
- User-friendly error messages in responses
- Logging to console with timestamps

---

### OCR & Entity Extraction
**Q12: How does the OCR process work?**
A:
1. EasyOCR reads image and detects text regions
2. Extracts text with confidence score (0-100%)
3. Returns raw OCR text string
4. Preprocess image first: grayscale → denoise → adaptive thresholding
5. Return (text, confidence_percentage) tuple

**Q13: What's your OCR confidence calculation?**
A:
- EasyOCR provides confidence scores per detected text region
- Average confidence across all regions
- Convert to percentage (multiply by 100)
- Return in response as "confidence_score"

**Q14: How do you extract entities from OCR text?**
A: Using regex patterns and keyword matching:
- **Email**: Regex `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
- **Mobile**: Multiple patterns for +91, 0, +, 10-digit formats
- **Website**: www/http/https domain patterns
- **Company**: Keywords (Ltd, Pvt, Inc, Corp, Co., LLC, LLP)
- **Designation**: 20+ keywords (director, manager, engineer, etc.)
- **Address**: Lines after "Address:" keyword or final 2 lines
- **Name**: Usually first/second line with capitalized words

**Q15: What if OCR fails to extract text?**
A:
- Return 400 Bad Request with "Could not extract text from image"
- Delete uploaded file
- Log error with details
- Frontend shows error message to user

---

### Database
**Q16: Describe the Contact model.**
A:
```
Table: contacts
Columns:
- id (INTEGER, PRIMARY KEY, auto-increment)
- name (VARCHAR, NOT NULL)
- designation (VARCHAR, nullable)
- company_name (VARCHAR, nullable)
- mobile (VARCHAR, nullable)
- email (VARCHAR, nullable)
- website (VARCHAR, nullable)
- address (TEXT, nullable)
- raw_text (TEXT)
- confidence_score (INTEGER)
- image_path (VARCHAR)
- created_at (TIMESTAMP, default: now)
- updated_at (TIMESTAMP, default: now, auto-update)
```

**Q17: How do you create tables automatically?**
A:
```python
Base.metadata.create_all(bind=engine)
```
Called in main.py on startup. SQLAlchemy creates tables from ORM models if they don't exist.

**Q18: Why use SQLite instead of PostgreSQL?**
A:
- Lightweight, no server setup needed
- File-based (visiting_cards.db in project root)
- Perfect for development/testing
- Easy to backup (single file)
- Sufficient for current scale (<1000 contacts)
- Scalability: Can migrate to PostgreSQL later without code changes (same SQLAlchemy ORM)

**Q19: How do you handle database sessions?**
A:
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
FastAPI dependency injection ensures session cleanup after each request.

---

### Testing & Validation
**Q20: How do you validate file uploads?**
A:
- Client-side: Check file type and size (10MB limit)
- Server-side: Validate using PIL/OpenCV
- Check file extension (jpg, png, pdf)
- Try to open image to verify integrity
- Fallback: If PIL fails, try cv2.imread()

**Q21: What data validation is used?**
A:
- Pydantic schemas validate all requests/responses
- ContactCreate requires: name (string, non-empty)
- ContactUpdate allows partial updates
- ContactResponse includes timestamps and id
- All schemas use from_attributes=True for ORM model conversion

**Q22: How do you generate test data?**
A: Created `generate_test_cards.py` script that:
- Generates 6 realistic visiting card images using PIL
- Each card: 900x500px JPG with gradient backgrounds
- Includes: company name, person name, designation, contact info
- Saves to `test_cards/` directory
- Used for testing upload workflow without real images

---

### Deployment & Performance
**Q23: How do you run the server?**
A:
```bash
python run.py
```
Which executes:
```python
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Q24: What's the server startup sequence?**
A:
1. Create database tables (if not exist)
2. Initialize FastAPI app
3. Add CORS middleware
4. Mount static files (/static, /uploads)
5. Include API routers
6. Define HTML page routes
7. Start Uvicorn server on port 8000

**Q25: How do you handle concurrent uploads?**
A:
- Each upload gets unique filename: `{timestamp}_{original_name}`
- File saved before processing (no race conditions)
- Database transactions via SQLAlchemy session
- OCR Reader is thread-safe (EasyOCR)

**Q26: What's the typical response time?**
A:
- File upload: <100ms
- OCR extraction: 2-5 seconds (depends on image size, CPU)
- Entity extraction: <100ms
- Database save: <50ms
- Total: ~2-5 seconds per card

---

### Static File Serving
**Q27: How do you serve frontend files?**
A:
- Mount frontend directory at `/static` using StaticFiles
- Mount uploads directory at `/uploads` for image serving
- HTML pages served via dedicated routes (/, /upload.html, /index.html)
- CSS and JS served via FileResponse with correct media types
- All paths are absolute (/styles.css, /app.js) to avoid relative path issues

**Q28: How are uploaded images accessible?**
A:
- Stored in `backend/uploads/` directory
- Mounted at `/uploads` route in FastAPI
- API returns HTTP URL: `/uploads/{filename}`
- Frontend displays via `<img src="/uploads/filename">`

---

### Security & Best Practices
**Q29: What security measures are implemented?**
A:
- File type validation (whitelist: jpg, png, pdf)
- File size limit (10MB max)
- Filename sanitization (timestamp prefix prevents overwrites)
- No direct file path exposure (returns HTTP URLs)
- CORS configured to allow frontend
- Input validation via Pydantic schemas
- Error messages don't expose sensitive info

**Q30: How do you handle edge cases?**
A:
- Empty file upload: Return 400 with "No file provided"
- Invalid image: Return 400 with "Invalid image format"
- OCR fails: Return 400 with "Could not extract text"
- Duplicate contact: Return special response with existing_id
- Contact not found: Return 404
- Database error: Return 500 with error details

---

## Technology Stack & Dependencies

### Core Framework
- **FastAPI 0.104.1**: Modern Python web framework for building APIs
- **Uvicorn 0.24.0**: ASGI server for running FastAPI

### Database
- **SQLAlchemy 2.0.23**: ORM for database operations
- **SQLite3**: Lightweight file-based database

### OCR & Image Processing
- **EasyOCR >=1.7.1**: Optical Character Recognition using deep learning
- **Pillow >=10.0.0**: Image processing and manipulation
- **OpenCV (opencv-python) 4.8.1.78**: Image preprocessing and validation
- **PyTorch 2.1.1**: Deep learning framework (required by EasyOCR)
- **TorchVision 0.16.1**: Computer vision utilities (required by EasyOCR)

### Natural Language Processing
- **spaCy 3.7.2**: NLP library (installed but regex-based extraction is primary)
- **regex 2023.11.4**: Advanced regex patterns for entity extraction

### Data Validation & Serialization
- **Pydantic 2.5.0**: Data validation and settings management
- **pydantic-settings 2.1.0**: Settings management from environment variables
- **python-multipart 0.0.6**: Multipart form data parsing for file uploads

### Environment Management
- **python-dotenv 1.0.0**: Load environment variables from .env file

### Middleware
- **CORS (built-in to FastAPI)**: Cross-Origin Resource Sharing support

---

## File Structure
```
pythonocr/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app setup, routes
│   │   ├── database.py             # SQLAlchemy config, session
│   │   ├── models/
│   │   │   └── __init__.py         # Contact ORM model
│   │   ├── routes/
│   │   │   └── visiting_card.py    # 7 API endpoints
│   │   ├── services/
│   │   │   ├── ocr_service.py      # OCR text extraction
│   │   │   └── contact_service.py  # Database CRUD
│   │   ├── utils/
│   │   │   └── entity_extractor.py # Regex entity extraction
│   │   └── schemas/
│   │       └── __init__.py         # Pydantic validation schemas
│   └── uploads/                    # Uploaded card images
├── frontend/
│   ├── home.html                   # Landing page
│   ├── upload.html                 # Upload interface
│   ├── index.html                  # Dashboard
│   ├── samples.html                # Sample cards
│   ├── styles.css                  # Unified styling
│   ├── app.js                      # Dashboard logic
│   ├── upload.js                   # Upload workflow
│   └── home.js                     # Landing page logic
├── test_cards/                     # Generated test images
├── .venv/                          # Python virtual environment
├── requirements.txt                # Python dependencies
├── run.py                          # Server launcher
├── generate_test_cards.py          # Test image generator
├── visiting_cards.db               # SQLite database
└── PROJECT_DOCUMENTATION.md        # This file
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip or conda
- ~2GB free disk space (for PyTorch models)

### Step-by-step Setup
```bash
# 1. Clone/navigate to project
cd /home/shubham/dbsl-internal/PythonPj/pythonocr

# 2. Create virtual environment
python3 -m venv .venv

# 3. Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Generate test cards (optional)
python generate_test_cards.py

# 6. Run server
python run.py

# 7. Access in browser
- Frontend: http://localhost:8000
- Upload: http://localhost:8000/upload.html
- Dashboard: http://localhost:8000/index.html
- API Docs: http://localhost:8000/docs
```

---

## Key Implementation Details

### Request/Response Format

**Upload Request:**
```
POST /api/v1/visiting-card/upload
Content-Type: multipart/form-data

file: <binary_image_data>
```

**Upload Response (Success):**
```json
{
    "status": "success",
    "message": "Contact created successfully",
    "contact_id": 1,
    "extracted_data": {
        "name": "John Doe",
        "designation": "Sales Director",
        "company_name": "TechVision Inc.",
        "mobile": "+91-9876543210",
        "email": "john@techvision.com",
        "website": "www.techvision.com",
        "address": "123 Tech Street, Silicon Valley",
        "ocr_confidence": "95%",
        "image_path": "/uploads/1781269698.861858_card.jpg"
    }
}
```

**Upload Response (Duplicate):**
```json
{
    "status": "duplicate",
    "message": "Contact already exists",
    "existing_id": 5,
    "extracted_data": { /* same as above */ }
}
```

### Entity Extraction Examples

**Input (OCR Text):**
```
TECHVISION INC.
John Doe
Sales Director
john@techvision.com
+91-9876543210
www.techvision.com
123 Tech Street, Silicon Valley, CA 94025
```

**Output (Extracted Entities):**
```python
{
    "name": "John Doe",
    "designation": "Sales Director",
    "company_name": "TechVision Inc.",
    "email": "john@techvision.com",
    "mobile": "+91-9876543210",
    "website": "www.techvision.com",
    "address": "123 Tech Street, Silicon Valley, CA 94025"
}
```

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| 404 Not Found for images | Images stored in file system, not HTTP accessible | Mount uploads directory at `/uploads` route |
| ANTIALIAS error | Pillow version conflict with EasyOCR | Use Pillow >=10.0.0 with EasyOCR >=1.7.1 |
| Slow OCR processing | CPU-only inference, large models | Consider GPU acceleration or image resizing |
| Database locked | Multiple writes simultaneously | SQLite has row-level locking; use PostgreSQL for high concurrency |
| Frontend CSS not loading | Relative paths in HTML | Use absolute paths (/styles.css) |
| CORS errors | Frontend and API on different origins | Enable CORS middleware in FastAPI |

---

## Performance Optimization Tips

1. **OCR Speed**: Resize images before OCR (current: 1-5s per card)
2. **Database**: Add indexes on email, mobile for faster duplicate detection
3. **Frontend**: Cache API responses in localStorage for offline support
4. **File Uploads**: Implement async upload with progress bar
5. **Scalability**: Move to PostgreSQL, add Redis caching layer

---

## Future Enhancement Ideas

1. **Batch OCR**: Process multiple cards simultaneously
2. **ML Training**: Fine-tune entity extraction with custom models
3. **Contact Enrichment**: Fetch company info from APIs (LinkedIn, Crunchbase)
4. **Export**: Generate Excel/CSV reports of contacts
5. **Mobile App**: React Native or Flutter mobile client
6. **Multi-language**: Support non-English visiting cards
7. **Verification**: Validate emails/phone numbers
8. **Analytics**: Track upload patterns, accuracy metrics
9. **Authentication**: Add user accounts, role-based access
10. **Webhooks**: Send notifications on new contacts

---

## Debugging Commands

```bash
# Check if server is running
lsof -i :8000

# Kill server process
kill -9 <PID>

# View database
sqlite3 visiting_cards.db ".tables"
sqlite3 visiting_cards.db "SELECT * FROM contacts;"

# Check logs
tail -f /var/log/application.log

# Test API endpoint
curl http://localhost:8000/health

# Generate test data
python generate_test_cards.py

# Install packages
pip install -r requirements.txt

# Freeze current dependencies
pip freeze > requirements.txt
```

---

## Contributors
- Full-stack development, OCR integration, database design
- Frontend UI/UX design
- Entity extraction algorithm

## License
Proprietary - Internal Use Only

---

**Last Updated**: 2026-06-12
**Project Status**: ✅ Complete & Functional
