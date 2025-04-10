from fastapi import Request, HTTPException, status
import json
from app.core.logging import LogEntry
from app.core.security import sanitize_mongo_query
from typing import Dict, Any

class RequestValidator:
    """
    Middleware para validar y sanitizar solicitudes
    """
    
    async def __call__(self, request: Request, call_next):
        # Solo procesar solicitudes POST, PUT o PATCH con JSON
        if request.method in ["POST", "PUT", "PATCH"] and "application/json" in request.headers.get("content-type", ""):
            # Leer y validar cuerpo de la solicitud
            try:
                body = await request.body()
                json_body = json.loads(body)
                
                # Validar tamaño máximo (5MB)
                if len(body) > 5 * 1024 * 1024:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail="El tamaño del cuerpo de la solicitud excede el límite permitido"
                    )
                
                # Buscar patrones maliciosos
                self._check_for_malicious_patterns(json_body)
                
                # Sanitizar consultas MongoDB si existe la clave 'query'
                if isinstance(json_body, dict) and 'query' in json_body and isinstance(json_body['query'], dict):
                    json_body['query'] = sanitize_mongo_query(json_body['query'])
                
                # Reemplazar el cuerpo de la solicitud con la versión sanitizada
                # Esto es un hack y no es ideal en FastAPI, pero es una solución simple para este ejemplo
                # En producción, sería mejor usar dependencias para procesar el cuerpo
                setattr(request, "_body", json.dumps(json_body).encode())
                
            except json.JSONDecodeError:
                # Registrar el error
                LogEntry("invalid_json_body", "warning") \
                    .add_data("path", request.url.path) \
                    .add_data("method", request.method) \
                    .log()
                    
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cuerpo JSON inválido"
                )
            except HTTPException:
                raise
            except Exception as e:
                # Registrar otros errores
                LogEntry("request_validation_error", "error") \
                    .add_data("path", request.url.path) \
                    .add_data("method", request.method) \
                    .add_data("error", str(e)) \
                    .log()
                    
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Error al procesar la solicitud"
                )
        
        # Continuar con el siguiente middleware o endpoint
        return await call_next(request)
    
    def _check_for_malicious_patterns(self, data: Any) -> None:
        """
        Verifica patrones maliciosos en los datos
        """
        if isinstance(data, dict):
            for key, value in data.items():
                # Detectar inyección NoSQL
                if key.startswith('$') and key not in ['$gt', '$lt', '$gte', '$lte', '$eq', '$ne', '$in', '$nin']:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Operador no permitido: {key}"
                    )
                
                # Recursivamente verificar objetos anidados
                self._check_for_malicious_patterns(value)
                
        elif isinstance(data, list):
            for item in data:
                self._check_for_malicious_patterns(item)