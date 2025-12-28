import sqlite3
from typing import Optional, Dict
from .models import get_db_connection

class UserDB:
    
    @staticmethod
    def create_user(email: str, password_hash: str) -> Optional[int]:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email.lower().strip(), password_hash)
            )
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, email, password_hash, created_at FROM users WHERE email = ?",
            (email.lower().strip(),)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'email': row['email'],
                'password_hash': row['password_hash'],
                'created_at': row['created_at']
            }
        return None
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, email, password_hash, created_at FROM users WHERE id = ?",
            (user_id,)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'email': row['email'],
                'password_hash': row['password_hash'],
                'created_at': row['created_at']
            }
        return None
    
    @staticmethod
    def email_exists(email: str) -> bool:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM users WHERE email = ?", (email.lower().strip(),))
        exists = cursor.fetchone() is not None
        
        conn.close()
        return exists
