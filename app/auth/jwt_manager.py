import os
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24
JWT_REFRESH_EXPIRATION_DAYS = 7

class JWTManager:
    
    @staticmethod
    def generate_token(user_id: int, email: str) -> str:
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    @staticmethod
    def generate_refresh_token(user_id: int, email: str) -> str:
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.utcnow() + timedelta(days=JWT_REFRESH_EXPIRATION_DAYS),
            'iat': datetime.utcnow(),
            'type': 'refresh'
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict]:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            if payload.get('type') != 'access':
                return None
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def verify_refresh_token(token: str) -> Optional[Dict]:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            if payload.get('type') != 'refresh':
                return None
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> Optional[str]:
        payload = JWTManager.verify_refresh_token(refresh_token)
        if not payload:
            return None
        
        return JWTManager.generate_token(
            user_id=payload['user_id'],
            email=payload['email']
        )
    
    @staticmethod
    def get_user_from_token(token: str) -> Optional[Dict]:
        payload = JWTManager.verify_token(token)
        if not payload:
            return None
        
        return {
            'id': payload['user_id'],
            'email': payload['email']
        }

