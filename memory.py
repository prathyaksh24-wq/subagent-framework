import sqlite3
import os

DB_PATH = r"C:\agent\agent_memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table 1 — logs every action the agent takes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS action_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            action TEXT,
            result TEXT,
            success INTEGER,
            duration_seconds REAL
        )
    ''')

    # Table 2 — stores reflections after reviewing actions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reflections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            summary TEXT,
            mistakes TEXT,
            improvements TEXT,
            confidence_score REAL
        )
    ''')

    # Table 3 — stores user behaviour patterns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            pattern TEXT,
            frequency INTEGER,
            preferred_time TEXT,
            context TEXT
        )
    ''')

    # Table 4 — stores learned preferences
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            preference TEXT,
            confidence REAL,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("[OK] Memory database initialised at:", DB_PATH)

init_db()