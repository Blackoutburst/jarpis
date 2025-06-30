import sqlite3

db = sqlite3.connect("messages.db")
cursor = db.cursor()

def create_db():
    global db
    global cursor

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        content TEXT
    )
    """)
    
    db.commit()

def add_message_db(role, content):
    global db
    global cursor

    cursor.execute("""
    INSERT INTO messages (role, content)
    VALUES (?, ?)
    """, (
        role,
        content
    ))

    db.commit()

def get_messages_db():
    global cursor
    
    cursor.execute("""
    SELECT role, content
    FROM messages
    ORDER BY id DESC
    LIMIT 100
    """)

    rows = cursor.fetchall()
    
    return rows

    
