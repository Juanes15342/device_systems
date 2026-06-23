from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.database.connection import engine, Base
from app.models import user_model, device_model, loan_model

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {"name": "Users", "description": "Gestión de usuarios del sistema device_systems."},
    {"name": "Devices", "description": "Gestión de dispositivos disponibles para préstamo."},
    {"name": "Loans", "description": "Gestión de préstamos entre usuarios y dispositivos."},
]

app = FastAPI(
    title="device_systems API",
    description="""
## API REST para gestión de usuarios, dispositivos y préstamos

Sistema **device_systems** permite administrar:

- **Users** – usuarios del sistema (admin, support, user)
- **Devices** – dispositivos tecnológicos disponibles para préstamo
- **Loans** – préstamos que relacionan usuarios con dispositivos
    """,
    version="1.0",
    openapi_tags=tags_metadata,
    contact={"name": "device_systems", "email": "admin@devicesystems.com"},
    license_info={"name": "MIT"}
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errores = [
        {"campo": " -> ".join(str(e) for e in error["loc"]), "mensaje": error["msg"], "tipo": error["type"]}
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"detail": "Error de validación en los datos enviados", "errores": errores}
    )

app.include_router(user_router, prefix="/api/v1", tags=["Users"])
app.include_router(device_router, prefix="/api/v1", tags=["Devices"])
app.include_router(loan_router, prefix="/api/v1", tags=["Loans"])

@app.get("/", tags=["Root"])
def root():
    return {"message": "Bienvenido a device_systems API", "version": "1.0"}