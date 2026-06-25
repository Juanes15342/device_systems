
API REST construida con FastAPI, SQLAlchemy, Alembic y seguridad OAuth2/JWT para la gestión de usuarios, dispositivos y préstamos del sistema device_systems.

---

##  Tecnologías utilizadas

- Python 3.x · FastAPI · Uvicorn
- SQLAlchemy · Alembic · SQLite
- Pydantic v2
- Passlib (bcrypt) · python-jose (JWT)
- Slowapi (rate limiting)

---

##  Instalación

```bash
git clone https://github.com/TU_USUARIO/device_systems.git
cd device_systems
git checkout device_systems_security
python -m venv fastapi_env
.\fastapi_env\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Variables de entorno

Copia `.env.example` a `.env` y completa tus valores:

```env
SECRET_KEY=tu_clave_secreta_larga_y_aleatoria
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

>  El archivo `.env` nunca se sube al repositorio (está en `.gitignore`). Solo `.env.example` se versiona, como plantilla.

---

## 🗄️ Migraciones con Alembic

### Inicialización de Alembic

Se inicializó Alembic en la raíz del proyecto para gestionar el versionado de la base de datos:

```bash
alembic init alembic
```

### Configuración

Se configuró `alembic.ini` con la URL de conexión a SQLite:
```ini
sqlalchemy.url = sqlite:///./device_systems.db
```

Y se configuró `alembic/env.py` para reconocer la metadata de SQLAlchemy y los modelos del proyecto (`User`, `Device`, `Loan`).

### Generación y aplicación de migraciones

```bash
alembic revision --autogenerate -m "create devices and loans tables"
alembic upgrade head
```

Posteriormente, se generó una migración adicional para añadir los campos de autenticación al modelo `User`:

```bash
alembic revision --autogenerate -m "add authentication fields to users"
alembic upgrade head
```

![Migración Alembic](img/alembic_auth_migration.png)

### Historial de migraciones

```bash
alembic history
```

---

## ▶️ Ejecución del servidor

```bash
uvicorn app.main:app --reload
```

Documentación interactiva disponible en:
http://127.0.0.1:8000/docs

http://127.0.0.1:8000/redoc

---

##  Estructura del proyecto

![Estructura del proyecto](img/estructura_proyecto.png)
device_systems/

│── app/

│   │── main.py

│   │── auth/

│   │   │── auth_routes.py

│   │   │── auth_service.py

│   │   └── security.py

│   │── database/

│   │   └── connection.py

│   │── models/

│   │   │── user_model.py

│   │   │── device_model.py

│   │   └── loan_model.py

│   │── schemas/

│   │   │── user_schema.py

│   │   │── device_schema.py

│   │   │── loan_schema.py

│   │   └── auth_schema.py

│   │── routes/

│   │   │── user_routes.py

│   │   │── device_routes.py

│   │   └── loan_routes.py

│   │── services/

│   │   │── user_service.py

│   │   │── device_service.py

│   │   └── loan_service.py

│   │── dependencies/

│   │   │── database_dependency.py

│   │   │── user_dependencies.py

│   │   └── auth_dependency.py

│   └── middlewares/

│       │── request_middleware.py

│       └── rate_limiter.py

│── alembic/

│   └── versions/

│── .env.example

│── alembic.ini

│── img/

│── requirements.txt

└── README.md

---

##  Modelos y asociaciones

- **User** — usuarios del sistema (`id`, `name`, `email`, `hashed_password`, `role`, `is_active`, `created_at`)
- **Device** — dispositivos disponibles para préstamo (`id`, `name`, `serial_number`, `device_type`, `brand`, `is_available`, `created_at`)
- **Loan** — préstamos que relacionan usuarios y dispositivos (`id`, `user_id`, `device_id`, `loan_date`, `return_date`, `status`)

### Relaciones

```python
# User
loans = relationship("Loan", back_populates="user")

# Device
loans = relationship("Loan", back_populates="device")

# Loan
user = relationship("User", back_populates="loans")
device = relationship("Device", back_populates="loans")
```
User (1) ──────< (N) Loan (N) >────── (1) Device

---

##  Endpoints — Users

| Método | Endpoint | Descripción | Código |
|--------|----------|-------------|--------|
| GET | /api/v1/users | Lista usuarios (requiere autenticación) | 200 |
| GET | /api/v1/users/{user_id} | Obtiene usuario por ID (requiere autenticación) | 200 |
| GET | /api/v1/users/{user_id}/loans | Préstamos de un usuario | 200 |
| POST | /api/v1/users | Crea usuario | 201 |
| PUT | /api/v1/users/{user_id} | Actualiza usuario completo | 200 |
| PATCH | /api/v1/users/{user_id} | Actualiza usuario parcial | 200 |
| DELETE | /api/v1/users/{user_id} | Elimina usuario | 204 |

##  Endpoints — Devices

| Método | Endpoint | Descripción | Protección | Código |
|--------|----------|-------------|-------------|--------|
| GET | /api/v1/devices | Lista dispositivos (filtros: device_type, is_available, brand, search) | — | 200 |
| GET | /api/v1/devices/{device_id} | Obtiene dispositivo por ID | — | 200 |
| GET | /api/v1/devices/{device_id}/loans | Historial de préstamos del dispositivo | — | 200 |
| POST | /api/v1/devices | Crea dispositivo | Admin o support | 201 |
| PUT | /api/v1/devices/{device_id} | Actualiza dispositivo completo | Admin o support | 200 |
| PATCH | /api/v1/devices/{device_id} | Actualiza dispositivo parcial | Admin o support | 200 |
| DELETE | /api/v1/devices/{device_id} | Elimina dispositivo | Admin | 204 |

##  Endpoints — Loans

| Método | Endpoint | Descripción | Protección | Código |
|--------|----------|-------------|-------------|--------|
| GET | /api/v1/loans | Lista préstamos (filtro por status) | — | 200 |
| GET | /api/v1/loans/{loan_id} | Obtiene préstamo por ID | — | 200 |
| GET | /api/v1/loans/details | Préstamos con info de usuario y dispositivo (joins) | Admin o support | 200 |
| POST | /api/v1/loans | Crea préstamo (valida existencia y disponibilidad) | Usuario autenticado | 201 |
| PATCH | /api/v1/loans/{loan_id}/return | Devuelve un préstamo y libera el dispositivo | Admin o support | 200 |

---

##  Autenticación y autorización

### Roles disponibles
`admin` · `support` · `user`

### Endpoints de autenticación

| Método | Endpoint | Descripción | Límite |
|--------|----------|-------------|--------|
| POST | /api/v1/auth/register | Registra un usuario nuevo | 3/min |
| POST | /api/v1/auth/login | Autentica y retorna JWT | 5/min |
| GET | /api/v1/auth/me | Datos del usuario autenticado | — |

---

##  Configuración CORS

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**¿Por qué no usar `allow_origins=["*"]` junto con `allow_credentials=True`?**

El estándar CORS prohíbe esta combinación porque, si cualquier origen pudiera enviar credenciales
(cookies, tokens en headers), un sitio malicioso podría hacer peticiones autenticadas a la API en
nombre de la víctima sin que ella lo note. Por eso los navegadores exigen una lista explícita de
orígenes confiables cuando se permiten credenciales, en lugar de aceptar un comodín.

---

##  Middleware personalizado

Cada respuesta incluye estas cabeceras, generadas por `RequestLoggingMiddleware`:
X-App-Name: device_systems

X-Process-Time: 0.0042

X-Request-ID: 8f42e9c1

Además, cada petición se registra en consola con método, ruta y código de estado.

![Cabeceras Middleware](img/cabeceras_middleware.png)

---

##  Rate Limiting

| Endpoint | Límite |
|----------|--------|
| POST /auth/login | 5 por minuto |
| POST /auth/register | 3 por minuto |
| GET /users | 30 por minuto |
| POST /loans | 10 por minuto |

Al superar el límite, la API responde `429 Too Many Requests`.

![Rate Limiting](img/rate_limiting.png)

---

##  Evidencias funcionales

### Registro de usuario
![Registro](img/registro_usuario.png)

### Login y token generado
![Login](img/login_token.png)

### Consulta /auth/me
![Auth Me](img/auth_me.png)

### Acceso sin token
![Sin Token](img/sin_token.png)

### Acceso con rol no permitido
![Rol No Permitido](img/rol_no_permitido.png)

### Swagger/OpenAPI con OAuth2
![Swagger OAuth2](img/swagger_oauth2.png)

### Consulta con joins — préstamos con información relacionada
`GET /api/v1/loans/details` usa `join()` entre `Loan`, `User` y `Device`, retornando el detalle anidado de cada relación.
![Loans Details](img/loans_details.png)

### Filtros aplicados
`GET /api/v1/loans?status=active` y `GET /api/v1/devices?device_type=laptop` usan `ilike()` para búsquedas insensibles a mayúsculas y `and_()`/`or_()` para combinar condiciones.
![Filtro Loans](img/filtro_loans.png)

### Devolución de dispositivo
`PATCH /api/v1/loans/1/return` marca el préstamo como `returned`, asigna `return_date` y libera el dispositivo.
![Devolución Loan](img/devolucion_loan.png)

### Verificación de disponibilidad tras devolución
![Device Disponible](img/device_disponible.png)

---

##  Manejo de errores

| Caso | Código |
|------|--------|
| Registro/creación exitosa | 201 Created |
| Consulta/login exitosa | 200 OK |
| Eliminación exitosa | 204 No Content |
| Recurso no encontrado | 404 Not Found |
| Dato duplicado | 400 Bad Request |
| Sin token / token inválido | 401 Unauthorized |
| Sin permisos para la acción | 403 Forbidden |
| Regla de negocio incumplida | 409 Conflict |
| Error de validación | 422 Unprocessable Entity |
| Límite de peticiones excedido | 429 Too Many Requests |

---

##  Reflexión final

Las migraciones con Alembic permiten versionar los cambios en la estructura de la base de datos de forma
controlada y reproducible, evitando modificar tablas manualmente y facilitando el trabajo en equipo. Las
relaciones entre modelos (`relationship()` y `ForeignKey`) permiten representar de forma natural cómo
los datos del mundo real se conectan entre sí, manteniendo la integridad referencial de la base de datos.
Las consultas avanzadas con `join()`, `and_()`, `or_()` e `ilike()` permiten construir respuestas enriquecidas
que combinan información de varias tablas en una sola petición.

Sumado a esto, la seguridad en una API REST no es un complemento opcional, sino una capa estructural que
determina si el sistema puede usarse en un entorno real. Implementar autenticación con OAuth2 y JWT permite
que cada cliente demuestre su identidad sin que el servidor tenga que recordar sesiones. El hash de
contraseñas con bcrypt garantiza que, incluso si la base de datos fuera comprometida, las contraseñas
originales permanezcan protegidas. La autorización basada en roles asegura que cada usuario solo pueda
realizar las acciones que le corresponden. El middleware de trazabilidad, las cabeceras personalizadas y
el rate limiting protegen la API de abuso y facilitan su monitoreo. Configurar CORS correctamente, sin
combinar comodines con credenciales, evita exponer la API a peticiones maliciosas desde dominios no
autorizados. En conjunto, estas prácticas transforman una API funcional en una API production-ready,
capaz de proteger tanto los datos del sistema como la confianza de quienes la consumen.