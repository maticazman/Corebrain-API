from typing import TypeVar, Generic, List, Optional, Dict, Any, Type
from datetime import datetime
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from bson import ObjectId
from bson.errors import InvalidId

# Tipo genérico para modelos
T = TypeVar('T', bound=BaseModel)

class BaseRepository(Generic[T]):
    """
    Repositorio base para operaciones CRUD genéricas
    """
    
    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str, model_class: Type[T]):
        self.db = db
        self.collection_name = collection_name
        self.collection = db[collection_name]
        self.model_class = model_class
    
    async def create(self, item: T) -> T:
        """
        Crea un nuevo documento
        """
        item_dict = item.model_dump(by_alias=True)
        await self.collection.insert_one(item_dict)
        return item
    
    async def find_by_id(self, id: str) -> Optional[T]:
        """
        Busca un documento por su ID
        """
        try:
            document = await self.collection.find_one({"id": id})
            if document:
                return self.model_class(**document)
            return None
        except Exception:
            return None
    
    async def find_one(self, query: Dict[str, Any]) -> Optional[T]:
        """
        Busca un documento según un filtro
        """
        document = await self.collection.find_one(query)
        if document:
            print("Encuentra el documento: ", document)
            return self.model_class(**document)
        return None
    
    async def find_many(self, query: Dict[str, Any], limit: int = 100, skip: int = 0) -> List[T]:
        """
        Busca múltiples documentos según un filtro
        """
        cursor = self.collection.find(query).skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        return [self.model_class(**document) for document in documents]
    
    async def update(self, id: str, item_update: BaseModel) -> Optional[T]:
        """
        Actualiza un documento por su ID
        """
        # Obtener solo los campos que se están actualizando (no nulos)
        update_data = item_update.model_dump(exclude_unset=True, exclude_none=True)
        
        if not update_data:
            return await self.find_by_id(id)
        
        # Añadir timestamp de actualización
        update_data["updated_at"] = datetime.now()
        
        # Realizar actualización
        result = await self.collection.update_one(
            {"id": id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            # Verificar si el documento existe
            exists = await self.find_by_id(id)
            if not exists:
                return None
        
        # Devolver documento actualizado
        return await self.find_by_id(id)
    
    async def delete(self, id: str) -> bool:
        """
        Elimina un documento por su ID
        """
        result = await self.collection.delete_one({"id": id})
        return result.deleted_count > 0
    
    async def count(self, query: Dict[str, Any]) -> int:
        """
        Cuenta documentos según un filtro
        """
        return await self.collection.count_documents(query)