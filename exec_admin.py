import asyncio
from app.services.auth_service import create_user, create_api_key
from app.models.user import UserCreate
from app.models.api_key import ApiKeyCreate

async def setup_client_with_api_key(email, name, password, key_name, key_level="write"):
    # 1. Crear usuario
    try:
        user_data = UserCreate(
            email=email,
            name=name,
            password=password
        )
        
        user = await create_user(user_data)
        print(f"Usuario creado: {user.id} ({user.email})")
        
        # 2. Crear API Key asociada
        api_key_data = ApiKeyCreate(
            name=key_name,
            user_id=user.id,
            level=key_level
        )
        
        api_key = await create_api_key(api_key_data)
        
        print("\n=== ACCESO CREADO EXITOSAMENTE ===")
        print(f"Usuario: {user.email}")
        print(f"ID de usuario: {user.id}")
        print(f"API Key: {api_key.key}")
        print(f"Nivel de acceso: {api_key.level}")
        print("==================================")
        
        return {
            "user": user,
            "api_key": api_key
        }
    
    except Exception as e:
        print(f"Error al crear acceso: {str(e)}")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    client_info = {
        "email": "ruben@globodain.com",
        "name": "Rubén Ayuso",
        "password": "abcabc123",
        "key_name": "API Principal Admin",
        "key_level": "admin"  # Niveles: "read", "write" o "admin"
    }
    
    result = asyncio.run(setup_client_with_api_key(
        client_info["email"],
        client_info["name"],
        client_info["password"],
        client_info["key_name"],
        client_info["key_level"]
    ))