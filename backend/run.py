#!/usr/bin/env python3
"""
The Royal Banquet Palace - Entry point runner script.
Usage:
    python backend/run.py
"""
import sys
import os

# Add project root to sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import uvicorn
from backend.app.config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"API Documentation available at: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"Connecting to database: {settings.DATABASE_URL}")
    uvicorn.run(
        "backend.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
