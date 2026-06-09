from app.database.connection import SessionLocal
from fastapi import Response

def agregar_cabeceras(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()