from fastapi import FastAPI
from app.routes.user_routes import router

app = FastAPI(
    title="device_systems API",
    description="API REST para gestión de usuarios del sistema device_systems",
    version="1.0",
)

app.include_router(router, prefix="/api/v1", tags=["Usuarios"])

@app.get("/")
def root():
    return {"message": "Bienvenido a device_systems API", "version": "1.0"}