# How to Check Your Data

## Database Location

All data is stored in: **`saas_app.db`** (SQLite database file in the project root)

## Database Structure

The database contains 4 tables:

1. **`users`** - User accounts
   - id, email, password_hash, created_at, updated_at

2. **`content_history`** - Generated content
   - id, user_id, title, prompt, output, content_type, tone, timestamp

3. **`user_preferences`** - User settings (future use)
   - id, user_id, default_content_type, default_tone, default_audience, default_length

4. **`usage_tracking`** - Usage logs (future use)
   - id, user_id, action_type, timestamp

## Method 1: Using the Python Script (Easiest)

Run the provided script:

```bash
python view_database.py
```

This will show:
- All users
- All content history
- User preferences
- Usage tracking
- Statistics

## Method 2: Using SQLite Command Line

### Windows PowerShell:
```powershell
sqlite3 saas_app.db
```

Then run SQL queries:
```sql
.tables                    -- List all tables
.schema users              -- Show users table structure
SELECT * FROM users;       -- View all users
SELECT * FROM content_history;  -- View all content
.quit                      -- Exit
```

### If sqlite3 is not installed:
```powershell
# Install via Python
python -m pip install sqlite3
```

## Method 3: Using Python Directly

```python
import sqlite3
from app.database.models import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

# View users
cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

# View content history
cursor.execute("SELECT * FROM content_history")
print(cursor.fetchall())

conn.close()
```

## Method 4: Using DB Browser (GUI Tool)

1. Download DB Browser for SQLite: https://sqlitebrowser.org/
2. Open `saas_app.db`
3. Browse tables and data visually
4. Run SQL queries in the SQL tab

## Method 5: View Specific User Data

```python
from app.database import UserDB, HistoryDB

# Get user by email
user = UserDB.get_user_by_email("user@example.com")
print(user)

# Get user's content history
history = HistoryDB.get_user_history(user_id=1)
print(history)
```

## Common Queries

### Count total users:
```sql
SELECT COUNT(*) FROM users;
```

### Count content per user:
```sql
SELECT u.email, COUNT(ch.id) as content_count
FROM users u
LEFT JOIN content_history ch ON u.id = ch.user_id
GROUP BY u.id;
```

### View recent content:
```sql
SELECT * FROM content_history 
ORDER BY timestamp DESC 
LIMIT 10;
```

### View content by user:
```sql
SELECT ch.*, u.email 
FROM content_history ch
JOIN users u ON ch.user_id = u.id
WHERE u.email = 'user@example.com';
```

## Security Note

- Passwords are hashed (bcrypt) - you cannot see plain text passwords
- Each user can only see their own data in the app
- Database file is in the project root - keep it secure

## Backup Database

To backup:
```bash
# Windows
copy saas_app.db saas_app_backup.db

# Or using Python
import shutil
shutil.copy('saas_app.db', 'saas_app_backup.db')
```

## Reset Database

To start fresh (WARNING: Deletes all data):
```bash
# Delete the database file
del saas_app.db

# Restart the app - it will recreate the database
```

