import json
import time
from typing import List, Dict, Any, Optional, Union, Tuple
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import OperationFailure
from app.core.config import settings
from app.core.logging import LogEntry
from app.core.cache import Cache
from app.core.security import sanitize_mongo_query
from app.core.permissions import verify_permissions, check_collection_access
from app.models.database_query import MongoDBQuery, QueryResult, AIQueryResponse
import anthropic

db_client = AsyncIOMotorClient(settings.MONGODB.MONGODB_URL)
db = db_client[settings.MONGODB.MONGODB_DB_NAME]

async def get_collection_names() -> List[str]:
    """Obtiene los nombres de todas las colecciones en la base de datos"""
    return await db.list_collection_names()

async def get_collection_schema(collection_name: str, sample_size: int = 5) -> Dict[str, Any]:
    """
    Infiere el esquema de una colección basado en una muestra de documentos
    
    Args:
        collection_name: Nombre de la colección
        sample_size: Cantidad de documentos a analizar
        
    Returns:
        Esquema inferido con tipos de datos
    """
    collection = db[collection_name]
    
    # Obtener una muestra de documentos
    cursor = collection.find().limit(sample_size)
    documents = await cursor.to_list(length=sample_size)
    
    if not documents:
        return {}
    
    # Analizar estructura
    schema = {}
    
    for doc in documents:
        for key, value in doc.items():
            if key == "_id":  # Omitir campo _id
                continue
                
            # Determinar tipo
            value_type = type(value).__name__
            
            if key not in schema:
                schema[key] = {
                    "type": value_type,
                    "example": str(value)[:50] + ("..." if len(str(value)) > 50 else "")
                }
            else:
                # Si ya existe pero con otro tipo, marcarlo como mixto
                if schema[key]["type"] != value_type:
                    schema[key]["type"] = f"mixed({schema[key]['type']}, {value_type})"
    
    return schema

async def execute_query(
    collection_name: str, 
    query: Dict[str, Any], 
    api_key_level: str,
    projection: Optional[Dict[str, int]] = None,
    sort: Optional[Dict[str, int]] = None,
    limit: int = 100,
    skip: int = 0
) -> QueryResult:
    """
    Ejecuta una consulta find en una colección específica
    
    Args:
        collection_name: Nombre de la colección
        query: Filtro de la consulta
        api_key_level: Nivel de permisos del API key
        projection: Campos a incluir/excluir
        sort: Ordenamiento
        limit: Límite de resultados
        skip: Cantidad de resultados a saltar
        
    Returns:
        Resultado de la consulta
    """
    start_time = time.time()
    
    # Verificar permisos de acceso a la colección
    if not check_collection_access(api_key_level, collection_name):
        raise PermissionError(f"Sin acceso a la colección: {collection_name}")
    
    # Sanitizar la consulta
    safe_query = sanitize_mongo_query(query)
    
    try:
        collection = db[collection_name]
        
        # Contar total de documentos que coinciden (para pagination)
        total_count = await collection.count_documents(safe_query)
        
        # Ejecutar consulta
        cursor = collection.find(
            filter=safe_query,
            projection=projection
        )
        
        # Aplicar sort, skip y limit
        if sort:
            cursor = cursor.sort(list(sort.items()))
        
        cursor = cursor.skip(skip).limit(limit)
        
        # Convertir a lista
        results = await cursor.to_list(length=limit)
        
        # Convertir ObjectId a string para serialización JSON
        for doc in results:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
        
        # Calcular tiempo de ejecución
        query_time = (time.time() - start_time) * 1000  # ms
        
        return QueryResult(
            data=results,
            count=len(results),
            query_time_ms=query_time,
            has_more=total_count > skip + limit,
            metadata={
                "total_count": total_count,
                "skip": skip,
                "limit": limit,
                "collection": collection_name
            }
        )
    
    except Exception as e:
        # Registrar error
        LogEntry("db_query_error", "error") \
            .add_data("collection", collection_name) \
            .add_data("error", str(e)) \
            .log()
        
        raise

async def execute_aggregation(
    collection_name: str,
    pipeline: List[Dict[str, Any]],
    api_key_level: str
) -> QueryResult:
    """
    Ejecuta una agregación en una colección específica
    
    Args:
        collection_name: Nombre de la colección
        pipeline: Pipeline de agregación
        api_key_level: Nivel de permisos del API key
        
    Returns:
        Resultado de la agregación
    """
    start_time = time.time()
    
    # Verificar permisos de acceso a la colección
    if not check_collection_access(api_key_level, collection_name):
        raise PermissionError(f"Sin acceso a la colección: {collection_name}")
    
    # Sanitizar el pipeline
    safe_pipeline = [sanitize_mongo_query(stage) for stage in pipeline]
    
    try:
        collection = db[collection_name]
        
        # Ejecutar agregación
        cursor = collection.aggregate(safe_pipeline)
        
        # Convertir a lista
        results = await cursor.to_list(length=None)
        
        # Convertir ObjectId a string para serialización JSON
        for doc in results:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
        
        # Calcular tiempo de ejecución
        query_time = (time.time() - start_time) * 1000  # ms
        
        return QueryResult(
            data=results,
            count=len(results),
            query_time_ms=query_time,
            has_more=False,  # No aplicable para agregaciones
            metadata={
                "collection": collection_name,
                "pipeline_stages": len(safe_pipeline)
            }
        )
    
    except Exception as e:
        # Registrar error
        LogEntry("db_aggregation_error", "error") \
            .add_data("collection", collection_name) \
            .add_data("error", str(e)) \
            .log()
        
        raise

async def get_database_name():
    """
    Retorna el nombre de la base de datos actual
    """
    # Asumiendo que db_service tiene acceso a la conexión de la base de datos
    # o al cliente de MongoDB
    return db_client.get_database().name

async def get_collection(collection_name: str):
    """
    Obtiene una referencia a una colección específica de la base de datos
    
    Args:
        collection_name: Nombre de la colección a obtener
        
    Returns:
        La colección de MongoDB solicitada
    """
    db = db_client.get_database()
    return db[collection_name]

async def get_database_info() -> Dict[str, Any]:
    """
    Obtiene información general sobre la base de datos
    """
    # Intentar obtener de caché
    cache_key = Cache.generate_key("db_info")
    cached_info = Cache.get(cache_key)
    
    if cached_info:
        return cached_info
    
    result = {"collections": {}}
    
    # Obtener nombres de colecciones
    collections = await get_collection_names()
    
    for collection_name in collections:
        collection = db[collection_name]
        
        # Obtener conteo de documentos
        count = await collection.count_documents({})
        
        # Obtener esquema inferido
        schema = await get_collection_schema(collection_name)
        
        # Agregar a resultado
        result["collections"][collection_name] = {
            "document_count": count,
            "schema": schema
        }
    
    # Guardar en caché (10 minutos)
    Cache.set(cache_key, result, ttl=600)
    
    return result

async def process_natural_language_query(
    query: str, 
    user_id: Optional[str],
    api_key_id: str,
    api_key_level: str,
    collection_name: Optional[str] = None
) -> AIQueryResponse:
    """
    Procesa una consulta en lenguaje natural y la convierte en operaciones MongoDB
    
    Args:
        query: Consulta en lenguaje natural
        user_id: ID del usuario (opcional)
        api_key_id: ID de la API key
        api_key_level: Nivel de permisos de la API key
        collection_name: Nombre de colección específica (opcional)
        
    Returns:
        Resultado de la consulta procesada por IA
    """
    start_time = time.time()
    
    # Verificar permisos básicos
    verify_permissions(api_key_level, "read")
    
    # Si se especifica una colección, verificar acceso
    if collection_name and not check_collection_access(api_key_level, collection_name):
        raise PermissionError(f"Sin acceso a la colección: {collection_name}")
    
    # Obtener información de la base de datos para contexto
    db_info = await get_database_info()
    
    # Si se especifica una colección, filtrar la información
    if collection_name:
        if collection_name in db_info["collections"]:
            db_info["collections"] = {collection_name: db_info["collections"][collection_name]}
        else:
            raise ValueError(f"Colección no encontrada: {collection_name}")
    
    # Convertir información de la base de datos a formato JSON para el prompt
    db_context = json.dumps(db_info, indent=2)
    
    # Limitar el contexto si es demasiado grande
    if len(db_context) > 10000:
        # Truncar y mostrar solo las primeras colecciones
        collections = list(db_info["collections"].keys())
        truncated_collections = collections[:5]
        
        truncated_db_info = {
            "collections": {
                name: db_info["collections"][name]
                for name in truncated_collections
            }
        }
        
        db_context = json.dumps(truncated_db_info, indent=2)
        db_context += f"\n\n... y {len(collections) - 5} colecciones más."
    
    # Generar prompt para Anthropic
    system_prompt = f"""
    Eres un asistente especializado en traducir consultas en lenguaje natural a operaciones MongoDB.
    
    Información sobre la base de datos:
    {db_context}
    
    Tu tarea es:
    1. Analizar la consulta del usuario
    2. Determinar qué colección debe ser consultada
    3. Construir la consulta apropiada (find o aggregate)
    4. Devolver la consulta como un objeto JSON con el siguiente formato:
    
    Para búsquedas simples:
    {{
      "collection": "nombre_coleccion",
      "operation": "find",
      "query": {{ /* filtros */ }},
      "projection": {{ /* campos a incluir/excluir */ }},
      "sort": {{ /* ordenamiento */ }},
      "limit": 10
    }}
    
    Para agregaciones:
    {{
      "collection": "nombre_coleccion",
      "operation": "aggregate",
      "pipeline": [
        {{ /* etapa 1 */ }},
        {{ /* etapa 2 */ }}
      ]
    }}
    
    Responde ÚNICAMENTE con el objeto JSON, sin ningún otro texto.
    """
    
    # Intentar obtener de caché
    cache_key = Cache.generate_key("nl_query", query, collection_name)
    cached_response = Cache.get(cache_key)
    
    mongo_query = None
    if cached_response:
        mongo_query = MongoDBQuery(**cached_response)
        
        # Registrar uso de caché
        LogEntry("nl_query_cache_hit") \
            .set_user_id(user_id) \
            .set_api_key_id(api_key_id) \
            .log()
    else:
        # Inicializar cliente Anthropic
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC.ANTHROPIC_API_KEY)
        
        try:
            # Enviar solicitud a Anthropic
            response = client.messages.create(
                model=settings.ANTHROPIC.ANTHROPIC_MODEL,
                max_tokens=settings.ANTHROPIC.MAX_TOKENS,
                temperature=0.2,  # Temperatura más baja para respuestas más deterministas
                messages=[{"role": "user", "content": query}],
                system=system_prompt
            )
            
            # Extraer respuesta JSON
            ai_response = response.content[0].text
            
            # Limpiar respuesta (eliminar backticks y otros caracteres)
            json_text = ai_response.strip()
            if json_text.startswith('```') and json_text.endswith('```'):
                json_text = json_text[3:-3].strip()
            if json_text.startswith('json'):
                json_text = json_text[4:].strip()
            
            # Parsear JSON
            query_data = json.loads(json_text)
            
            # Crear objeto MongoDBQuery
            mongo_query = MongoDBQuery(
                collection=query_data["collection"],
                operation=query_data["operation"],
                query=query_data.get("query"),
                pipeline=query_data.get("pipeline"),
                limit=query_data.get("limit", 10),
                skip=query_data.get("skip", 0),
                sort=query_data.get("sort")
            )
            
            # Guardar en caché (1 hora)
            Cache.set(cache_key, mongo_query.model_dump(), ttl=3600)
            
        except Exception as e:
            # Registrar error
            LogEntry("nl_query_translation_error", "error") \
                .set_user_id(user_id) \
                .set_api_key_id(api_key_id) \
                .add_data("query", query) \
                .add_data("error", str(e)) \
                .log()
            
            raise ValueError(f"Error al traducir consulta: {str(e)}")
    
    # Ejecutar la consulta MongoDB
    if mongo_query.operation == "find":
        result = await execute_query(
            collection_name=mongo_query.collection,
            query=mongo_query.query or {},
            api_key_level=api_key_level,
            sort=mongo_query.sort,
            limit=mongo_query.limit,
            skip=mongo_query.skip
        )
    elif mongo_query.operation == "aggregate":
        result = await execute_aggregation(
            collection_name=mongo_query.collection,
            pipeline=mongo_query.pipeline or [],
            api_key_level=api_key_level
        )
    else:
        raise ValueError(f"Operación no soportada: {mongo_query.operation}")
    
    # Generar explicación de resultados
    explanation = await generate_result_explanation(query, mongo_query, result)
    
    # Calcular tiempo total de procesamiento
    processing_time = time.time() - start_time
    
    # Registrar consulta exitosa
    LogEntry("nl_query_processed") \
        .set_user_id(user_id) \
        .set_api_key_id(api_key_id) \
        .add_data("query", query) \
        .add_data("collection", mongo_query.collection) \
        .add_data("operation", mongo_query.operation) \
        .add_data("processing_time", processing_time) \
        .add_data("result_count", result.count) \
        .log()
    
    # Crear respuesta final
    return AIQueryResponse(
        natural_query=query,
        mongo_query=mongo_query,
        result=result,
        explanation=explanation,
        metadata={
            "processing_time": processing_time,
            "anthropic_model": settings.ANTHROPIC.ANTHROPIC_MODEL
        }
    )

async def generate_result_explanation(
    query: str,
    mongo_query: MongoDBQuery,
    result: QueryResult
) -> str:
    """
    Genera una explicación en lenguaje natural de los resultados de una consulta
    
    Args:
        query: Consulta original en lenguaje natural
        mongo_query: Consulta MongoDB generada
        result: Resultado de la consulta
        
    Returns:
        Explicación en lenguaje natural
    """
    # Limitar resultado para el prompt
    result_sample = result.data[:5]
    
    # Preparar contexto
    context = {
        "original_query": query,
        "mongodb_query": mongo_query.model_dump(),
        "result_count": result.count,
        "total_count": result.metadata.get("total_count", result.count),
        "result_sample": result_sample,
        "query_time_ms": result.query_time_ms
    }
    
    context_json = json.dumps(context, indent=2)
    
    # Generar prompt para Anthropic
    system_prompt = """
    Eres un asistente especializado en explicar resultados de consultas a bases de datos.
    Debes explicar los resultados de manera clara y concisa, destacando los aspectos más relevantes.
    
    Algunas pautas:
    1. Menciona cuántos resultados se encontraron
    2. Resume los hallazgos principales
    3. Si hay pocos o ningún resultado, sugiere posibles razones
    4. Evita tecnicismos innecesarios
    5. Sé breve y directo
    """
    
    try:
        # Inicializar cliente Anthropic
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC.ANTHROPIC_API_KEY)
        
        # Enviar solicitud a Anthropic
        response = client.messages.create(
            model=settings.ANTHROPIC.ANTHROPIC_MODEL,
            max_tokens=settings.ANTHROPIC.MAX_TOKENS,
            temperature=0.7,
            messages=[{"role": "user", "content": f"Explica los siguientes resultados de consulta:\n{context_json}"}],
            system=system_prompt
        )
        
        # Extraer explicación
        explanation = response.content[0].text
        
        return explanation
    
    except Exception as e:
        # En caso de error, generar explicación básica
        if result.count == 0:
            return "No se encontraron resultados para tu consulta."
        else:
            return f"Se encontraron {result.count} resultados en la colección {mongo_query.collection}."
