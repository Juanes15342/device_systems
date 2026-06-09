from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routes.user_routes import router
from app.database.connection import engine, Base
from app.models import user_model

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="""
## API REST para gestión de usuarios

Sistema **device_systems** permite administrar usuarios con los siguientes roles:

- **admin** – Administrador del sistema
- **support** – Soporte técnico  
- **user** – Usuario estándar

### Funcionalidades
- Crear, listar, actualizar y eliminar usuarios
- Filtrar por rol y estado
- Ordenar por nombre o fecha de creación
- Validación completa de datos con Pydantic
    """,
    version="1.0",
    contact={
        "name": "device_systems",
        "email": "admin@devicesystems.com"
    },
    license_info={
        "name": "MIT"
    }
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errores = []
    for error in exc.errors():
        errores.append({
            "campo": " -> ".join(str(e) for e in error["loc"]),
            "mensaje": error["msg"],
            "tipo": error["type"]
        })
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Error de validación en los datos enviados",
            "errores": errores
        }
    )

app.include_router(router, prefix="/api/v1", tags=["Usuarios"])

@app.get("/", tags=["Root"])
def root():
    return {"message": "Bienvenido a device_systems API", "version": "1.0"}