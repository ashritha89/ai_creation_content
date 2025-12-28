import re
import bcrypt
from typing import Optional, Tuple
from app.database.user_db import UserDB

class AuthManager:
    
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, Optional[str]]:
        if not email or not email.strip():
            return False, "Email is required"
        
        email = email.lower().strip()
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format"
        
        if len(email) > 255:
            return False, "Email is too long"
        
        return True, None
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, Optional[str]]:
        if not password:
            return False, "Password is required"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        if len(password) > 128:
            return False, "Password is too long"
        
        return True, None
    
    @staticmethod
    def register_user(email: str, password: str) -> Tuple[bool, Optional[str], Optional[int]]:
        email_valid, email_error = AuthManager.validate_email(email)
        if not email_valid:
            return False, email_error, None
        
        password_valid, password_error = AuthManager.validate_password(password)
        if not password_valid:
            return False, password_error, None
        
        if UserDB.email_exists(email):
            return False, "Email already registered", None
        
        password_hash = AuthManager.hash_password(password)
        
        user_id = UserDB.create_user(email, password_hash)
        
        if user_id:
            return True, None, user_id
        else:
            return False, "Failed to create user. Email may already exist.", None
    
    @staticmethod
    def login_user(email: str, password: str) -> Tuple[bool, Optional[str], Optional[dict]]:
        email_valid, email_error = AuthManager.validate_email(email)
        if not email_valid:
            return False, email_error, None
        
        user = UserDB.get_user_by_email(email)
        
        if not user:
            return False, "Invalid email or password", None
        
        if not AuthManager.verify_password(password, user['password_hash']):
            return False, "Invalid email or password", None
        
        user_data = {
            'id': user['id'],
            'email': user['email'],
            'created_at': user['created_at']
        }
        
        return True, None, user_data
