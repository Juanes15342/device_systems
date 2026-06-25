from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.database.connection import engine, Base
from app.models import user_model, device_model, loan_model
from app.auth.auth_routes import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.middlewares.request_middleware import RequestLoggingMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {"name": "Auth", "description": "Registro, login y consulta del usuario autenticado mediante JWT."},
    {"name": "Users", "description": "Gestión de usuarios del sistema device_systems."},
    {"name": "Devices", "description": "Gestión de dispositivos disponibles para préstamo."},
    {"name": "Loans", "description": "Gestión de préstamos entre usuarios y dispositivos."},
    {"name": "Security", "description": "Información sobre las medidas de seguridad implementadas: CORS, rate limiting y middleware."},
]

app = FastAPI(
    title="device_systems API",
    description="""
## API REST segura para gestión de usuarios, dispositivos y préstamos

Incluye autenticación OAuth2 con JWT, hash de contraseñas, control de acceso por roles,
CORS configurado, middleware de trazabilidad y rate limiting.
    """,
    version="3.0.0",
    openapi_tags=tags_metadata,
    contact={"name": "device_systems", "email": "admin@devicesystems.com"},
    license_info={"name": "MIT"}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite (React/Vue)
        "http://localhost:3000",  # Create React App / Next.js
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
app.include_router(auth_router, prefix="/api/v1", tags=["Auth"])
app.add_middleware(RequestLoggingMiddleware)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get(
    "/api/v1/security/info",
    tags=["Security"],
    summary="Información de seguridad",
    description="Resumen de las medidas de seguridad implementadas en la API."
)
def security_info():
    return {
        "authentication": "OAuth2 + JWT",
        "password_hashing": "bcrypt (passlib)",
        "cors_enabled": True,
        "rate_limiting": "slowapi",
        "roles": ["admin", "support", "user"]
    }