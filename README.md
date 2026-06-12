# Visiting Card OCR Scanner & Data Extraction System

A complete OCR-based system for scanning, extracting, and managing visiting card information.

## Features

✅ **OCR Text Extraction** - Extract text from visiting card images using EasyOCR  
✅ **Entity Recognition** - Automatically identify name, email, phone, company, etc.  
✅ **Duplicate Detection** - Prevent duplicate entries by email or mobile number  
✅ **Database Management** - Store and retrieve contact information  
✅ **RESTful API** - Complete API for all operations  
✅ **Interactive Frontend** - Upload, view, search, and manage contacts  
✅ **Image Preprocessing** - Enhance image quality for better OCR results  

## Project Structure

```
pythonocr/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── routes/          # API routes
│   │   ├── services/        # Business logic
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── utils/           # Utility functions
│   │   ├── main.py          # FastAPI app
│   │   └── database.py      # Database config
│   ├── uploads/             # Uploaded images
│   ├── requirements.txt     # Python dependencies
│   └── run.py              # Start server
├── frontend/
│   ├── index.html          # Dashboard
│   ├── upload.html         # Upload page
│   ├── app.js              # Dashboard logic
│   ├── upload.js           # Upload logic
│   └── styles.css          # Styles
└── README.md
```

## System Requirements

- Python 3.8+
- pip (Python package manager)
- Modern web browser
- ~2GB disk space for OCR models

## Installation

### 1. Install Python Dependencies

```bash
cd /home/shubham/dbsl-internal/PythonPj/pythonocr
pip install -r requirements.txt
```

This will install:
- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database
- **EasyOCR** - OCR engine
- **OpenCV** - Image processing
- **Pillow** - Image manipulation
- **spaCy** - NLP library
- And other dependencies

### 2. Download spaCy Language Model (Optional)

For advanced NER capabilities:

```bash
python -m spacy download en_core_web_sm
```

## Configuration

Create a `.env` file in the backend directory (optional):

```bash
# backend/.env
DATABASE_URL=sqlite:///./visiting_cards.db
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=*
LOG_LEVEL=INFO
```

## Running the Application

### Backend Server

```bash
cd backend
python app/main.py
```

Or using uvicorn directly:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### Frontend

Open your browser and navigate to:

- **Dashboard**: Open `frontend/index.html`
- **Upload**: Open `frontend/upload.html`
- **API Docs**: `http://localhost:8000/docs`

## API Endpoints

### Visiting Card Operations

```
POST   /api/v1/visiting-card/upload    - Upload and process a visiting card
GET    /api/v1/contacts                 - Get all contacts (paginated)
GET    /api/v1/contact/{id}             - Get specific contact
PUT    /api/v1/contact/{id}             - Update contact
DELETE /api/v1/contact/{id}             - Delete contact
GET    /api/v1/contacts/search?q=...    - Search contacts
```

### Health Check

```
GET    /health                           - Check API health
GET    /                                 - API info
```

## Usage Examples

### 1. Upload a Visiting Card

```bash
curl -X POST \
  -F "file=@visiting_card.jpg" \
  http://localhost:8000/api/v1/visiting-card/upload
```

**Response:**
```json
{
  "status": "success",
  "message": "Contact created successfully",
  "contact_id": 1,
  "extracted_data": {
    "name": "John Smith",
    "designation": "Sales Director",
    "company_name": "ABC Technologies Pvt Ltd",
    "mobile": "+919876543210",
    "email": "john.smith@abctech.com",
    "website": "www.abctech.com",
    "address": "Mumbai, Maharashtra",
    "ocr_confidence": "96%"
  }
}
```

### 2. Get All Contacts

```bash
curl http://localhost:8000/api/v1/contacts?skip=0&limit=10
```

### 3. Search Contacts

```bash
curl "http://localhost:8000/api/v1/contacts/search?q=john"
```

### 4. Get Contact Details

```bash
curl http://localhost:8000/api/v1/contact/1
```

### 5. Update Contact

```bash
curl -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "designation": "Senior Sales Director",
    "company_name": "ABC Tech"
  }' \
  http://localhost:8000/api/v1/contact/1
```

## Supported File Formats

- **JPG / JPEG**
- **PNG**
- **PDF**

Maximum file size: **10 MB**

## OCR Confidence Score

The system returns a confidence score (0-100%) indicating the reliability of the extracted text.

- **90-100%**: Highly accurate
- **70-90%**: Good accuracy
- **50-70%**: Fair accuracy (manual review recommended)
- **<50%**: Low accuracy (manual correction needed)

## Features Explained

### 1. Text Extraction

Uses EasyOCR to extract text from images with high accuracy. The engine supports multiple languages and handles various image qualities.

### 2. Entity Extraction

Extracts structured information using:
- **Regex Patterns**: For emails, phones, websites
- **Named Entity Recognition**: For names and locations
- **Keyword Matching**: For designations and company names

### 3. Duplicate Detection

Prevents duplicate entries by checking:
- Email address
- Mobile number

If a duplicate is found, user is prompted to either:
- Skip creation
- Create anyway (if needed for history)
- View existing contact

### 4. Image Preprocessing

Optional preprocessing includes:
- Grayscale conversion
- Noise reduction
- Adaptive thresholding
- Improves OCR accuracy for low-quality images

## Database Schema

### Contacts Table

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    designation VARCHAR(255),
    company_name VARCHAR(255),
    mobile VARCHAR(20) UNIQUE,
    email VARCHAR(255) UNIQUE,
    website VARCHAR(255),
    address TEXT,
    raw_text TEXT,
    confidence_score DECIMAL,
    image_path VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Troubleshooting

### Issue: "OCR Reader failed to initialize"

**Solution**: 
```bash
pip install --upgrade easyocr
pip install --upgrade torch
```

### Issue: "CORS error when accessing from frontend"

**Solution**: 
Check that the API server is running on `localhost:8000` and CORS is enabled in `main.py`

### Issue: "Slow OCR processing"

**Solution**:
- Reduce image size before upload
- Use GPU if available (modify OCR service)
- Pre-process images for better quality

### Issue: "Database locked"

**Solution**:
```bash
# Remove old database
rm visiting_cards.db
# Restart the server
```

## Performance Tips

1. **Image Quality**: Use high-resolution, well-lit card images
2. **Batch Processing**: Upload one card at a time for best results
3. **Database Optimization**: Regular database cleanup for large datasets
4. **Caching**: Implement caching for frequently accessed contacts

## Security Considerations

1. **File Upload**: Only accept image files (JPG, PNG, PDF)
2. **File Size**: Limit uploads to 10 MB
3. **CORS**: Configure CORS properly for production
4. **Authentication**: Add authentication layer for production
5. **Data Validation**: All inputs are validated

## Development

### Adding New Features

1. **New API Endpoint**: Add route in `app/routes/`
2. **Database Field**: Modify model in `app/models/`
3. **Business Logic**: Add service in `app/services/`
4. **Frontend**: Update HTML/JS in `frontend/`

### Testing

```bash
# Test API with curl
curl -X GET http://localhost:8000/health

# Test upload
curl -F "file=@test_card.jpg" http://localhost:8000/api/v1/visiting-card/upload
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| FastAPI | 0.104.1 | Web Framework |
| Uvicorn | 0.24.0 | ASGI Server |
| SQLAlchemy | 2.0.23 | ORM |
| EasyOCR | 1.7.0 | OCR Engine |
| OpenCV | 4.8.1.78 | Image Processing |
| Pillow | 10.1.0 | Image Manipulation |
| spaCy | 3.7.2 | NLP |
| Pydantic | 2.5.0 | Data Validation |

## License

This project is provided as-is for educational and business use.

## Support

For issues or questions, refer to:
- FastAPI: https://fastapi.tiangolo.com/
- EasyOCR: https://github.com/JaidedAI/EasyOCR
- SQLAlchemy: https://docs.sqlalchemy.org/

---

**Version**: 1.0.0  
**Last Updated**: 2024
