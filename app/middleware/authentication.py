
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import APIKeyHeader
from typing import Optional, Dict, Any, Tuple
import time
from app.core.config import settings
from app.core.logging import LogEntry
from app.services import auth_service
from app.models.api_key import ApiKeyInDB

# Definir el header de API key
API_KEY_HEADER = APIKeyHeader(name=settings.SECURITY.API_KEY_NAME)

async def get_api_key(
    api_key: str = Depends(API_KEY_HEADER)
) -> ApiKeyInDB:
    """
    Dependencia para obtener y validar la API key
    """
    try:
        # Validar API key
        api_key_data = await auth_service.get_api_key_data(api_key)
        
        if not api_key_data:
            # Registrar intento fallido
            LogEntry("api_key_validation_failed", "warning") \
                .add_data("key_prefix", api_key[:5] if api_key else None) \
                .log()
                
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key inválida o expirada"
            )
        
        # Registrar uso válido
        LogEntry("api_key_validation_success", "info") \
            .set_api_key_id(api_key_data.id) \
            .set_user_id(api_key_data.user_id) \
            .log()
        print("api_key_data a devolver: ", api_key_data)
        return api_key_data
    
    except HTTPException:
        raise
    except Exception as e:
        # Registrar error
        LogEntry("api_key_validation_error", "error") \
            .add_data("error", str(e)) \
            .log()
            
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al validar API key"
        )

class AuthenticationMiddleware:
    """
    Middleware para autenticación y registro de solicitudes
    """
    
    async def __call__(self, request: Request, call_next):
        # Generar ID único para la solicitud
        request_id = LogEntry("").request_id
        request.state.request_id = request_id
        
        # Registrar inicio de solicitud
        start_time = time.time()
        path = request.url.path
        method = request.method
        
        log_entry = LogEntry("request_started") \
            .add_data("path", path) \
            .add_data("method", method) \
            .add_data("request_id", request_id)
        
        # Extraer y registrar API key (si existe)
        api_key = request.headers.get(settings.SECURITY.API_KEY_NAME)
        if api_key:
            # Solo registramos los primeros 5 caracteres por seguridad
            log_entry.add_data("api_key_prefix", api_key[:5])
            
            # Intentar obtener información de la API key sin validar aún
            try:
                api_key_data = await auth_service.get_api_key_data(api_key, validate=False)
                if api_key_data:
                    request.state.api_key_data = api_key_data
                    log_entry.set_api_key_id(api_key_data.id)
                    log_entry.set_user_id(api_key_data.user_id)
            except:
                # Si hay error, continuamos sin datos de API key
                pass
        
        log_entry.log()
        
        # Procesar la solicitud
        try:
            response = await call_next(request)
            
            # Registrar finalización exitosa
            process_time = time.time() - start_time
            status_code = response.status_code
            
            LogEntry("request_completed") \
                .add_data("path", path) \
                .add_data("method", method) \
                .add_data("status_code", status_code) \
                .add_data("process_time_ms", round(process_time * 1000, 2)) \
                .add_data("request_id", request_id) \
                .set_api_key_id(getattr(request.state, "api_key_data", {}).get("id", None)) \
                .set_user_id(getattr(request.state, "api_key_data", {}).get("user_id", None)) \
                .log()
            
            return response
            
        except Exception as e:
            # Registrar error
            process_time = time.time() - start_time
            
            LogEntry("request_failed", "error") \
                .add_data("path", path) \
                .add_data("method", method) \
                .add_data("error", str(e)) \
                .add_data("process_time_ms", round(process_time * 1000, 2)) \
                .add_data("request_id", request_id) \
                .set_api_key_id(getattr(request.state, "api_key_data", {}).get("id", None)) \
                .set_user_id(getattr(request.state, "api_key_data", {}).get("user_id", None)) \
                .log()
            
            raise

