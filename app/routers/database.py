from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from typing import List, Optional, Dict, Any
from statistics import mean

from app.models.database_query import DatabaseQuery, AIQueryResponse
from app.services import db_service
from app.middleware.authentication import get_api_key
from app.core.permissions import verify_permissions, PermissionError
from app.core.logging import LogEntry

router = APIRouter()

@router.post("/query", response_model=AIQueryResponse)
async def natural_language_query(
    query_data: DatabaseQuery = Body(...),
    api_key = Depends(get_api_key)
):
    """
    Ejecuta una consulta en lenguaje natural sobre la base de datos
    
    # * Sólo puede ejecutar actualmente consultas a 1 collection.
    # * No permite multiples consultas en diferentes collections.
    """
    try:
        # Verificar permisos básicos
        verify_permissions(api_key.level, "read")
        
        # Procesar consulta
        response = await db_service.process_natural_language_query(
            query=query_data.query,
            user_id=None,  # No hay usuario en API key
            api_key_id=api_key.id,
            api_key_level=api_key.level,
            collection_name=query_data.collection_name
        )
        
        return response
        
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
    except Exception as e:
        LogEntry("database_query_error", "error") \
            .set_api_key_id(api_key.id) \
            .add_data("query", query_data.query) \
            .add_data("error", str(e)) \
            .log()
            
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar consulta"
        )


@router.get("/try", response_model=Dict[str, Any])
async def get_truth(
    api_key = Depends(get_api_key)
):
    """
    Obtiene información sobre las colecciones y esquemas de la base de datos
    y calcula estadísticas para las transacciones
    """
    try:
        print("Entra a la función")
        # Verificar permisos básicos
        verify_permissions(api_key.level, "read")
        print("Va al response data")
        # Preparar la respuesta estructurada
        response_data = {
            "status": "success",
            "message": "Información de la base de datos y estadísticas de transacciones",
            "database_info": {},
            "transaction_stats": {
                "aggregation_method": None,
                "accounts_processed": 0,
                "average_transaction_amount": None,
                "account_details": []
            }
        }

        # Obtener información de la base de datos para incluirla en la respuesta
        database = db_service.db

        # Acceder a la colección de transacciones
        transactions_collection = database['transactions']
        
        # Método 1: Usando agregación de MongoDB
        try:
            resultado_agregacion = await transactions_collection.aggregate([
                {
                    "$match": {
                        "transactions": { "$exists": True, "$ne": [] }
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "account_id": 1,
                        "media_amount": { "$avg": "$transactions.amount" }
                    }
                }
            ]).to_list(length=None)
            
            print("\nResultados de agregación:")
            
            if resultado_agregacion:
                # Imprimir resultados de la agregación
                total_media = 0
                contador = 0
                
                for doc in resultado_agregacion:
                    if 'media_amount' in doc:
                        total_media += doc['media_amount']
                        contador += 1
                        print(f"  Cuenta ID: {doc.get('account_id', 'No ID')} - Media: {doc['media_amount']}")
                        
                        # Añadir información a la respuesta
                        response_data["transaction_stats"]["account_details"].append({
                            "account_id": doc.get('account_id', 'No ID'),
                            "average_amount": doc['media_amount']
                        })
                
                if contador > 0:
                    average = total_media / contador
                    print(f"Media general para todas las transacciones: {average}")
                    
                    # Actualizar los datos de la respuesta
                    response_data["transaction_stats"]["aggregation_method"] = "MongoDB Aggregation"
                    response_data["transaction_stats"]["accounts_processed"] = contador
                    response_data["transaction_stats"]["average_transaction_amount"] = average
                else:
                    print(f"No se encontraron documentos con 'transactions.amount' en la colección")
                    response_data["transaction_stats"]["aggregation_method"] = "MongoDB Aggregation - No Data"
            else:
                print("  La agregación no devolvió resultados. Intentando método alternativo...")
                
                # Método 2: Procesar los datos en Python si la agregación no funciona
                from statistics import mean
                
                documentos = await transactions_collection.find(
                    {"transactions": {"$exists": True}}
                ).to_list(length=None)
                
                total_docs = 0
                sum_medias = 0
                
                for doc in documentos:
                    if 'transactions' in doc and isinstance(doc['transactions'], list) and doc['transactions']:
                        # Extraer todos los valores de 'amount'
                        try:
                            amounts = [t['amount'] for t in doc['transactions'] 
                                    if isinstance(t, dict) and 'amount' in t]
                            
                            if amounts:
                                media_amount = mean(amounts)
                                sum_medias += media_amount
                                total_docs += 1
                                print(f"  Cuenta ID: {doc.get('account_id', 'No ID')} - Media (Python): {media_amount}")
                                
                                # Añadir información a la respuesta
                                response_data["transaction_stats"]["account_details"].append({
                                    "account_id": doc.get('account_id', 'No ID'),
                                    "average_amount": media_amount
                                })
                        except Exception as e:
                            print(f"  Error al procesar documento: {str(e)}")
                
                if total_docs > 0:
                    python_average = sum_medias / total_docs
                    print(f"  Media general (calculada en Python): {python_average}")
                    
                    # Actualizar los datos de la respuesta
                    response_data["transaction_stats"]["aggregation_method"] = "Python Calculation"
                    response_data["transaction_stats"]["accounts_processed"] = total_docs
                    response_data["transaction_stats"]["average_transaction_amount"] = python_average
                else:
                    print(f"  No se encontraron documentos con 'transactions.amount' válidos")
                    response_data["transaction_stats"]["aggregation_method"] = "Python Calculation - No Data"
        
        except Exception as e:
            error_message = f"Error en el cálculo de estadísticas: {str(e)}"
            print(error_message)
            response_data["status"] = "partial_success"
            response_data["message"] = error_message
        
        # Retornar la respuesta estructurada
        return response_data
        
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
        
    except Exception as e:
        LogEntry("get_schema_error", "error") \
            .set_api_key_id(api_key.id) \
            .add_data("error", str(e)) \
            .log()
        print("Error: ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener esquema de la base de datos"
        )
        
@router.get("/collections", response_model=Dict[str, Any])
async def get_database_schema(
    api_key = Depends(get_api_key)
):
    """
    Obtiene información sobre las colecciones y esquemas de la base de datos
    """
    try:
        # Verificar permisos básicos
        verify_permissions(api_key.level, "read")

        # Obtener información de la base de datos
        db_info = await db_service.get_database_info()

        # Filtrar colecciones según permisos
        collections_to_remove = []

        for collection_name in db_info["collections"]:
            if not await db_service.check_collection_access(api_key.level, collection_name):
                collections_to_remove.append(collection_name)

        for collection_name in collections_to_remove:
            del db_info["collections"][collection_name]
            
        return db_info
        
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
        
    except Exception as e:
        LogEntry("get_schema_error", "error") \
            .set_api_key_id(api_key.id) \
            .add_data("error", str(e)) \
            .log()
            
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener esquema de la base de datos"
        )