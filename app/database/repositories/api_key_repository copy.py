from typing import List, Optional, Dict, Any
from datetime import datetime
from app.database.repositories.base_repository import BaseRepository
from app.models.api_key import ApiKeyInDB, ApiKeyUpdate

class ApiKeyRepository(BaseRepository[ApiKeyInDB]):
    """
    Repositorio para operaciones con API keys
    """
    
    def __init__(self, db):
        super().__init__(db, "api_keys", ApiKeyInDB)
    
    async def find_key_by_id(self, id: str) -> Optional[ApiKeyInDB]:
        """
        Busca una API key por su ID.
        
        Args:
            id: ID de la API key
            
        Returns:
            ApiKeyInDB o None
        """
        if hasattr(id, 'id') and isinstance(getattr(id, 'id'), str):
            id = getattr(id, 'id')

        return await self.find_one({"id": id})
    
    async def find_by_key(self, key: Any) -> Optional[ApiKeyInDB]:
        """
        Busca una API key por su valor.
        
        Args:
            key: Valor de la API key o objeto ApiKeyInDB
            
        Returns:
            ApiKeyInDB o None si no se encuentra
        """
        # Si key es un objeto con atributo 'key', extraer ese valor
        if hasattr(key, 'key') and isinstance(getattr(key, 'key'), str):
            key = getattr(key, 'key')
        
        # Verificar que ahora key sea un string
        if not isinstance(key, str):
            raise TypeError(f"Expected API key to be string, got {type(key)}")
        
        return await self.find_one({"key": key})
    
    async def find_by_user_id(self, user_id: str, include_inactive: bool = False) -> List[ApiKeyInDB]:
        """
        Busca las API keys de un usuario
        """
        query = {"user_id": user_id}
        
        if not include_inactive:
            query["active"] = True
        
        return await self.find_many(query)
    
    async def revoke_key(self, key_id: str) -> bool:
        """
        Revoca una API key (la marca como inactiva)
        """
        update = ApiKeyUpdate(active=False)
        result = await self.update(key_id, update)
        return result is not None
    
    async def update_usage(self, key_id: str) -> bool:
        """
        Actualiza las estadísticas de uso de una API key
        """
        update = ApiKeyUpdate(
            last_used_at=datetime.now(),
            usage_count={"$inc": 1}  # Incrementar contador
        )
        
        result = await self.collection.update_one(
            {"id": key_id},
            {"$set": {"last_used_at": update.last_used_at}, "$inc": {"usage_count": 1}}
        )
        
        return result.modified_count > 0
