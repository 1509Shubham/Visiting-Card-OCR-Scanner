#!/usr/bin/env python
"""
Run the Visiting Card OCR Scanner API Server
"""

import sys
import os
import uvicorn

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

if __name__ == "__main__":
    print("=" * 60)
    print("Visiting Card OCR Scanner - API Server")
    print("=" * 60)
    print("\nStarting server...")
    print("- API: http://localhost:8000")
    print("- Docs: http://localhost:8000/docs")
    print("- Frontend: Open frontend/index.html")
    print("\nPress CTRL+C to stop\n")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
