# device_systems API

API REST construida con FastAPI para la gestión de usuarios del sistema device_systems.

---

## 🛠️ Tecnologías utilizadas

- Python 3.x
- FastAPI
- Uvicorn
- Pydantic v2

---

## 📦 Instalación de dependencias

Clona el repositorio y activa el entorno virtual:

```bash
git clone https://github.com/TU_USUARIO/device_systems.git
cd device_systems
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Ejecución del servidor

```bash
uvicorn app.main:app --reload
```

Luego abre en tu navegador:
http://127.0.0.1:8000/docs

---

## 📋 Tabla de endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /api/v1/users | Lista todos los usuarios |
| GET | /api/v1/users/{user_id} | Obtiene un usuario por ID |
| GET | /api/v1/users?role=admin | Filtra usuarios por rol |
| GET | /api/v1/users?is_active=true | Filtra por estado activo |
| POST | /api/v1/users | Crea un nuevo usuario |

---

## 🔍 Ejemplos de peticiones

### GET /api/v1/users
http://127.0.0.1:8000/api/v1/users

### GET /api/v1/users/{user_id}
http://127.0.0.1:8000/api/v1/users/1

### GET con filtro por rol
http://127.0.0.1:8000/api/v1/users?role=admin

### POST /api/v1/users
```json
{
  "name": "Ana Nueva",
  "email": "ana@mail.com",
  "role": "user",
  "is_active": true
}
```

---

## 📸 Evidencias Swagger UI

### Interfaz general
![Swagger UI](img/swagger_ui.png)

### GET /api/v1/users — Listar todos los usuarios
![GET Users](img/get_users.png)

### GET /api/v1/users/{user_id} — Buscar por ID
![GET User por ID](img/get_user_id.png)

### GET /api/v1/users?role=admin — Filtro por rol
![GET Filtro Rol](img/get_users_filtro.png)

### POST /api/v1/users — Crear usuario
![POST User](img/post_user.png)

### Error 400 — Correo duplicado
![Error 400](img/error_400.png)

### Error 404 — Usuario no encontrado
![Error 404](img/error_404.png)

---

## 💡 Reflexión

FastAPI permite construir APIs REST de forma rápida y ordenada gracias a su integración
con Pydantic para validación de datos, la generación automática de documentación con
Swagger UI y el uso de tipado de Python para definir modelos de entrada y salida.
Durante este proyecto aprendí a estructurar una API con rutas, esquemas y modelos de
respuesta separados, aplicar validaciones, manejar errores HTTP y personalizar cabeceras,
lo que me da una base sólida para construir backends más complejos.