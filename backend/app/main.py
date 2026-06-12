import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.exc import SQLAlchemyError
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base, get_db
from app.routes import visiting_card
from app.models import Contact

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables created")

# Initialize FastAPI app
app = FastAPI(
    title="Visiting Card OCR Scanner",
    description="OCR-based system for scanning and extracting visiting card information",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup frontend path
frontend_dir = os.path.join(os.path.dirname(__file__), "../../frontend")
logger.info(f"Frontend directory: {frontend_dir}")

# Setup uploads directory
uploads_dir = os.path.join(os.path.dirname(__file__), "../../backend/uploads")
os.makedirs(uploads_dir, exist_ok=True)
logger.info(f"Uploads directory: {uploads_dir}")

# Mount static files BEFORE defining routes
if os.path.exists(uploads_dir):
    app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")
    logger.info("Uploads static files mounted successfully")

if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir, html=True), name="static")
    logger.info("Static files mounted successfully")

# Include API routers
app.include_router(visiting_card.router)


# Routes for HTML pages
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve home page"""
    home_path = os.path.join(frontend_dir, "home.html")
    if os.path.exists(home_path):
        with open(home_path, 'r', encoding='utf-8') as f:
            return f.read()
    return get_fallback_html("Visiting Card OCR Scanner")


@app.get("/home.html", response_class=HTMLResponse)
async def home_page():
    """Serve home page"""
    home_path = os.path.join(frontend_dir, "home.html")
    if os.path.exists(home_path):
        with open(home_path, 'r', encoding='utf-8') as f:
            return f.read()
    return get_fallback_html("Home")


@app.get("/index.html", response_class=HTMLResponse)
async def dashboard_page():
    """Serve dashboard page"""
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            return f.read()
    return get_fallback_html("Dashboard")


@app.get("/dashboard.html", response_class=HTMLResponse)
async def alt_dashboard_page():
    """Serve dashboard page (alternative route)"""
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            return f.read()
    return get_fallback_html("Dashboard")


@app.get("/upload.html", response_class=HTMLResponse)
async def upload_page():
    """Serve upload page"""
    upload_path = os.path.join(frontend_dir, "upload.html")
    if os.path.exists(upload_path):
        with open(upload_path, 'r', encoding='utf-8') as f:
            return f.read()
    return get_fallback_html("Upload")


@app.get("/styles.css")
async def styles():
    """Serve CSS"""
    css_path = os.path.join(frontend_dir, "styles.css")
    if os.path.exists(css_path):
        return FileResponse(css_path, media_type="text/css")
    return {"error": "CSS not found"}


@app.get("/app.js")
async def app_js():
    """Serve dashboard JS"""
    js_path = os.path.join(frontend_dir, "app.js")
    if os.path.exists(js_path):
        return FileResponse(js_path, media_type="application/javascript")
    return {"error": "JS not found"}


@app.get("/upload.js")
async def upload_js():
    """Serve upload JS"""
    js_path = os.path.join(frontend_dir, "upload.js")
    if os.path.exists(js_path):
        return FileResponse(js_path, media_type="application/javascript")
    return {"error": "JS not found"}


@app.get("/home.js")
async def home_js():
    """Serve home JS"""
    js_path = os.path.join(frontend_dir, "home.js")
    if os.path.exists(js_path):
        return FileResponse(js_path, media_type="application/javascript")
    return {"error": "JS not found"}


def get_fallback_html(page_title):
    """Get fallback HTML page"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{page_title} - Visiting Card OCR Scanner</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }}
            .container {{ text-align: center; color: white; padding: 20px; }}
            h1 {{ font-size: 48px; margin-bottom: 20px; }}
            p {{ font-size: 18px; margin-bottom: 30px; opacity: 0.9; }}
            .buttons {{ display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; }}
            a {{ padding: 12px 24px; background: white; color: #667eea; text-decoration: none; border-radius: 5px; font-weight: 600; transition: all 0.3s; display: inline-block; }}
            a:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Visiting Card OCR Scanner</h1>
            <p>Intelligent Visiting Card Recognition & Data Extraction</p>
            <div class="buttons">
                <a href="/">🏠 Home</a>
                <a href="/index.html">📊 Dashboard</a>
                <a href="/upload.html">📤 Upload Card</a>
                <a href="/docs">📚 API Docs</a>
            </div>
        </div>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        db = next(get_db())
        db.query(Contact).first()
        return {"status": "healthy", "database": "connected"}
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        return {"status": "unhealthy", "database": "disconnected"}
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {"status": "unhealthy", "error": str(e)}


@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info("Application started")
    logger.info("Initializing OCR reader...")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    logger.info("Application shutdown")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
