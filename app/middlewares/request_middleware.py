import time
import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("device_systems")
logging.basicConfig(level=logging.INFO)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Genera o propaga un Request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Cabeceras personalizadas
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        response.headers["X-Request-ID"] = request_id

        # Registro de la petición
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"-> {response.status_code} ({process_time:.4f}s)"
        )

        return response