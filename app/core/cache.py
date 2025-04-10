
import redis
from typing import Optional, Any, Union, Dict
import json
import pickle
from app.core.config import settings
import hashlib

# Cliente Redis
redis_client = redis.from_url(settings.CACHE.REDIS_URL)

class Cache:
    @staticmethod
    def generate_key(prefix: str, *args, **kwargs) -> str:
        """
        Genera una clave de caché a partir de parámetros
        """
        key_parts = [prefix]
        
        # Añadir args ordenados
        for arg in args:
            if isinstance(arg, (str, int, float, bool)):
                key_parts.append(str(arg))
            else:
                # Para objetos complejos, usar su representación JSON
                key_parts.append(hashlib.md5(json.dumps(arg, sort_keys=True).encode()).hexdigest())
        
        # Añadir kwargs ordenados por clave
        for k in sorted(kwargs.keys()):
            v = kwargs[k]
            key_parts.append(f"{k}:")
            if isinstance(v, (str, int, float, bool)):
                key_parts.append(str(v))
            else:
                # Para objetos complejos, usar su representación JSON
                key_parts.append(hashlib.md5(json.dumps(v, sort_keys=True).encode()).hexdigest())
        
        # Unir todas las partes con ':'
        key = ":".join(key_parts)
        
        # Aplicar hash MD5 para limitar longitud
        return hashlib.md5(key.encode()).hexdigest()
    
    @staticmethod
    def set(key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Almacena un valor en caché
        """
        if not settings.CACHE.ENABLE_CACHE:
            return False
        
        ttl = ttl if ttl is not None else settings.CACHE.CACHE_TTL
        
        try:
            # Convertir objetos complejos a bytes con pickle
            if not isinstance(value, (str, int, float, bool)):
                value = pickle.dumps(value)
            
            return redis_client.set(key, value, ex=ttl)
        except Exception as e:
            print(f"Error setting cache: {e}")
            return False
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """
        Recupera un valor de la caché
        """
        if not settings.CACHE.ENABLE_CACHE:
            return default
        
        try:
            value = redis_client.get(key)
            if value is None:
                return default
            
            # Intentar deserializar con pickle
            try:
                return pickle.loads(value)
            except Exception as e:
                print(e)
                # Si no es pickle, devolver como está
                return value
        except Exception as e:
            print(f"Error getting cache: {e}")
            return default
    
    @staticmethod
    def delete(key: str) -> bool:
        """
        Elimina una clave de la caché
        """
        if not settings.CACHE.ENABLE_CACHE:
            return False
        
        try:
            return redis_client.delete(key) > 0
        except Exception as e:
            print(f"Error deleting cache: {e}")
            return False
    
    @staticmethod
    def flush() -> bool:
        """
        Limpia toda la caché
        """
        if not settings.CACHE.ENABLE_CACHE:
            return False
        
        try:
            return redis_client.flushdb()
        except Exception as e:
            print(f"Error flushing cache: {e}")
            return False
