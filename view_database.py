import sqlite3
from app.database.models import get_db_connection

def view_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("=" * 80)
    print("DATABASE CONTENTS")
    print("=" * 80)
    
    print("\nUSERS TABLE")
    print("-" * 80)
    cursor.execute("SELECT id, email, created_at FROM users")
    users = cursor.fetchall()
    if users:
        print(f"{'ID':<5} {'Email':<40} {'Created At':<20}")
        print("-" * 80)
        for user in users:
            print(f"{user['id']:<5} {user['email']:<40} {user['created_at']:<20}")
    else:
        print("No users found")
    
    print("\nCONTENT HISTORY TABLE")
    print("-" * 80)
    cursor.execute("""
        SELECT ch.id, ch.user_id, u.email, ch.title, ch.content_type, ch.tone, ch.timestamp 
        FROM content_history ch
        LEFT JOIN users u ON ch.user_id = u.id
        ORDER BY ch.timestamp DESC
        LIMIT 20
    """)
    history = cursor.fetchall()
    if history:
        print(f"{'ID':<5} {'User ID':<8} {'Email':<30} {'Title':<30} {'Type':<15} {'Tone':<15} {'Timestamp':<20}")
        print("-" * 80)
        for item in history:
            title = item['title'][:28] + ".." if len(item['title']) > 30 else item['title']
            email = item['email'][:28] + ".." if item['email'] and len(item['email']) > 30 else (item['email'] or 'N/A')
            print(f"{item['id']:<5} {item['user_id']:<8} {email:<30} {title:<30} {item['content_type'] or 'N/A':<15} {item['tone'] or 'N/A':<15} {item['timestamp']:<20}")
    else:
        print("No content history found")
    
    print("\nUSER PREFERENCES TABLE")
    print("-" * 80)
    cursor.execute("SELECT * FROM user_preferences")
    preferences = cursor.fetchall()
    if preferences:
        for pref in preferences:
            print(f"User ID: {pref['user_id']}")
            print(f"  Default Content Type: {pref['default_content_type'] or 'None'}")
            print(f"  Default Tone: {pref['default_tone'] or 'None'}")
            print(f"  Default Audience: {pref['default_audience'] or 'None'}")
            print(f"  Default Length: {pref['default_length'] or 'None'}")
    else:
        print("No user preferences found")
    
    print("\nUSAGE TRACKING TABLE")
    print("-" * 80)
    cursor.execute("""
        SELECT ut.id, ut.user_id, u.email, ut.action_type, ut.timestamp 
        FROM usage_tracking ut
        LEFT JOIN users u ON ut.user_id = u.id
        ORDER BY ut.timestamp DESC
        LIMIT 20
    """)
    usage = cursor.fetchall()
    if usage:
        print(f"{'ID':<5} {'User ID':<8} {'Email':<30} {'Action':<20} {'Timestamp':<20}")
        print("-" * 80)
        for item in usage:
            email = item['email'][:28] + ".." if item['email'] and len(item['email']) > 30 else (item['email'] or 'N/A')
            print(f"{item['id']:<5} {item['user_id']:<8} {email:<30} {item['action_type']:<20} {item['timestamp']:<20}")
    else:
        print("No usage tracking data found")
    
    print("\n" + "=" * 80)
    print("STATISTICS")
    print("=" * 80)
    
    cursor.execute("SELECT COUNT(*) as count FROM users")
    user_count = cursor.fetchone()['count']
    print(f"Total Users: {user_count}")
    
    cursor.execute("SELECT COUNT(*) as count FROM content_history")
    content_count = cursor.fetchone()['count']
    print(f"Total Content Items: {content_count}")
    
    cursor.execute("SELECT COUNT(*) as count FROM usage_tracking")
    usage_count = cursor.fetchone()['count']
    print(f"Total Usage Records: {usage_count}")
    
    conn.close()

if __name__ == "__main__":
    view_database()

