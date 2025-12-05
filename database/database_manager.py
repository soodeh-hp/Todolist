import sqlite3

def create_database():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            title TEXT PRIMARY KEY,
            note TEXT,
            calendar TEXT,
            alarm_hour INTEGER,
            alarm_minute INTEGER
        )
    """)
    conn.commit()
    conn.close()
