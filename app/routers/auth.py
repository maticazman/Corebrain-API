from fastapi import APIRouter, Depends, HTTPException, status, Body, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, APIKeyHeader
from typing import List, Optional

from app.core.config import settings
from app.models.api_key import ApiKeyCreate, ApiKeyResponse, ApiKeyUpdate
from app.models.user import UserCreate, UserResponse, UserUpdate
from app.services import auth_service
from app.middleware.authentication import get_api_key
from app.core.permissions import verify_permissions
from app.core.logging import LogEntry

router = APIRouter()

# Para autenticación basada en JWT (dashboard)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Para autenticación basada en API key (SDK)
API_KEY_HEADER = APIKeyHeader(name=settings.SECURITY.API_KEY_NAME)

@router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Obtiene un token JWT de acceso (para dashboard)
    """
    print("Entra a la ruta")
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token(user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role
    }

@router.post("/users", response_model=UserResponse)
async def create_user(user_data: UserCreate):
    """
    Crea un nuevo usuario
    """
    try:
        user = await auth_service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/api-keys", response_model=ApiKeyResponse)
async def create_api_key(
    api_key_data: ApiKeyCreate,
    current_api_key = Depends(get_api_key)
):
    """
    Crea una nueva API key
    """
    # Verificar permisos
    verify_permissions(current_api_key.level, "admin")
    
    try:
        api_key = await auth_service.create_api_key(api_key_data)
        return api_key
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/api-keys/validate")
async def validate_api_key(
    request: Request,
    api_key: str = Depends(API_KEY_HEADER)
):
    """
    Valida una API key
    """
    print("Pasa al await get api key")
    api_key_data = getattr(request.state, "api_key_data", None)
    
    if not api_key_data:
        print("No hay datos en request.state, obteniendo directamente")
        try:
            api_key_data = await auth_service.get_api_key_data(api_key)
        except Exception as e:
            print("Error al obtener api key: ", e)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key inválida"
            )
        
    print("Pasa al return")
    return {
        "valid": True,
        "level": api_key_data.level,
        "name": api_key_data.name,
        "allowed_domains": api_key_data.allowed_domains
    }

@router.delete("/api-keys/{api_key_id}")
async def revoke_api_key(
    api_key_id: str,
    current_api_key = Depends(get_api_key)
):
    """
    Revoca una API key
    """
    # Verificar permisos
    verify_permissions(current_api_key.level, "admin")
    
    # Verificar que no está revocando su propia API key
    if current_api_key.id == api_key_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes revocar tu propia API key activa"
        )
    
    success = await auth_service.revoke_api_key(api_key_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key no encontrada"
        )
    
    return {"message": "API key revocada correctamente"}