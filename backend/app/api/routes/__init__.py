from app.api.routes import auth, health

# Note: `resume` and `tailor` routers are imported lazily by the application
# startup to allow the server to run in environments missing optional native
# dependencies (OCR, Pillow, python-docx). See `app.main` for lazy import.
__all__ = ["auth", "health"]
