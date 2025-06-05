# app/lib/sso/client.py
from fastapi import FastAPI, Request, HTTPException, status, Response
from fastapi.responses import RedirectResponse
from functools import wraps
from urllib.parse import urlencode
from typing import Callable, Optional, Dict, Any
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings
from app.core.logging import logging

import requests

class GlobodainSSOAuth:
    def __init__(self, app: Optional[FastAPI] = None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: FastAPI):
        # Cargar configuración desde settings
        self.sso_url = settings.SSO.GLOBODAIN_SSO_URL
        self.client_id = settings.SSO.GLOBODAIN_CLIENT_ID
        self.client_secret = settings.SSO.GLOBODAIN_CLIENT_SECRET
        self.redirect_uri = settings.SSO.GLOBODAIN_REDIRECT_URI
        self.success_redirect = settings.SSO.GLOBODAIN_SUCCESS_REDIRECT
        self.secret_key = settings.SECURITY.SECRET_KEY
        self.algorithm = "HS256"

    def create_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Crear un token JWT para el usuario autenticado por SSO"""
        to_encode = data.copy()
        
        # Establecer tiempo de expiración
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=15)
            
        to_encode.update({"exp": expire})
        
        # Agregar indicador de origen SSO
        to_encode.update({"sso_provider": "globodain"})
        
        # Codificar con JWT
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def get_login_url(self, state: Optional[str] = None) -> str:
        """Generar la URL de inicio de sesión para el SSO"""
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
        }
        
        # Usar el parámetro state para almacenar la URL de redireccionamiento
        if state:
            params['state'] = state
            
        return f"{self.sso_url}/api/auth/authorize?{urlencode(params)}"

    def login_required(self, func: Callable) -> Callable:
        """Decorador para rutas que requieren autenticación mediante SSO"""
        @wraps(func)
        async def decorated_function(request: Request, *args, **kwargs):
            # Verificar si ya hay un token de autenticación
            auth_header = request.headers.get("Authorization")
            
            if not auth_header or not auth_header.startswith("Bearer "):
                # No hay token, redirigir al SSO
                return_url = str(request.url)
                redirect_url = self.get_login_url(return_url)
                return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
                
            # Existe token, verificar con tu middleware de autenticación existente
            return await func(request, *args, **kwargs)
        return decorated_function

    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verificar token con el servidor SSO"""
        try:
            response = requests.post(
                f"{self.sso_url}/api/auth/service-auth",
                headers={'Authorization': f'Bearer {token}'},
                json={'service_id': self.client_id}
            )
            if response.status_code == 200:
                logging.info("Token ha sido verificado. Procediendo a consultar datos de usuario")
                return response.json()
            return None
        except Exception as e:
            logging.error(f"Error verificando token: {str(e)}")
            return None

    async def get_user_info(self, token: str) -> Optional[Dict[str, Any]]:
        """Obtener información del usuario con el token"""
        try:
            response = requests.get(
                f"{self.sso_url}/api/users/me/profile",
                headers={'Authorization': f'Bearer {token}'}
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logging.error(f"Error obteniendo info de usuario: {str(e)}")
            return None

    async def exchange_code_for_token(self, code: str) -> Optional[Dict[str, Any]]:
        """Intercambiar código de autorización por token de acceso"""
        try:
            response = requests.post(
                f"{self.sso_url}/api/auth/token",
                json={
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'code': code,
                    'grant_type': 'authorization_code',
                    'redirect_uri': self.redirect_uri
                }
            )
            if response.status_code == 200:
                return response.json()
            logging.error(f"Error en exchange_code_for_token: {response.status_code} - {response.text}")
            return None
        except Exception as e:
            logging.error(f"Error intercambiando código: {str(e)}")
            return None