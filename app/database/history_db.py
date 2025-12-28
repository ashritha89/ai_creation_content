from typing import List, Dict, Optional
from .models import get_db_connection

class HistoryDB:
    
    @staticmethod
    def save_content(
        user_id: int,
        title: str,
        prompt: str,
        output: str,
        content_type: Optional[str] = None,
        tone: Optional[str] = None
    ) -> int:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO content_history 
               (user_id, title, prompt, output, content_type, tone) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, title, prompt, output, content_type, tone)
        )
        
        history_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return history_id
    
    @staticmethod
    def get_user_history(user_id: int, limit: int = 50) -> List[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT id, title, prompt, output, content_type, tone, timestamp 
               FROM content_history 
               WHERE user_id = ? 
               ORDER BY timestamp DESC 
               LIMIT ?""",
            (user_id, limit)
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row['id'],
                'title': row['title'],
                'prompt': row['prompt'],
                'output': row['output'],
                'content_type': row['content_type'],
                'tone': row['tone'],
                'timestamp': row['timestamp']
            }
            for row in rows
        ]
    
    @staticmethod
    def delete_content(user_id: int, content_id: int) -> bool:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "DELETE FROM content_history WHERE id = ? AND user_id = ?",
            (content_id, user_id)
        )
        
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return deleted
    
    @staticmethod
    def get_content_by_id(user_id: int, content_id: int) -> Optional[Dict]:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT id, title, prompt, output, content_type, tone, timestamp 
               FROM content_history 
               WHERE id = ? AND user_id = ?""",
            (content_id, user_id)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'title': row['title'],
                'prompt': row['prompt'],
                'output': row['output'],
                'content_type': row['content_type'],
                'tone': row['tone'],
                'timestamp': row['timestamp']
            }
        return None
