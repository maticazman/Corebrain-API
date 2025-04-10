from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Union

class DatabaseQuery(BaseModel):
    query: str  # Consulta en lenguaje natural
    collection_name: Optional[str] = None  # Si se especifica, limitar a esta colección
    limit: int = 10
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MongoDBQuery(BaseModel):
    collection: str
    operation: str  # "find", "aggregate", "count", etc.
    query: Optional[Dict[str, Any]] = None
    pipeline: Optional[List[Dict[str, Any]]] = None
    limit: int = 10
    skip: int = 0
    sort: Optional[Dict[str, int]] = None

class QueryResult(BaseModel):
    data: List[Dict[str, Any]]
    count: int
    query_time_ms: float
    has_more: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AIQueryResponse(BaseModel):
    natural_query: str
    mongo_query: MongoDBQuery
    result: QueryResult
    explanation: str
    metadata: Dict[str, Any] = Field(default_factory=dict)