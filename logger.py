import sqlite3
import time
import os
from datetime import datetime

DB_PATH = r"C:\agent\agent_memory.db"

def log_action(action, result, success, duration=0.0):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO action_log (action, result, success, duration_seconds)
        VALUES (?, ?, ?, ?)
    ''', (action, result, int(success), duration))
    conn.commit()
    conn.close()
    print(f"[LOGGED] {action} → {'OK' if success else 'FAIL'}")

def log_user_pattern(pattern, context="", preferred_time=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if pattern already exists and increment frequency
    cursor.execute('SELECT id, frequency FROM user_profile WHERE pattern = ?', (pattern,))
    row = cursor.fetchone()

    if row:
        cursor.execute('''
            UPDATE user_profile 
            SET frequency = ?, preferred_time = ?, context = ?
            WHERE id = ?
        ''', (row[1] + 1, preferred_time, context, row[0]))
    else:
        cursor.execute('''
            INSERT INTO user_profile (pattern, frequency, preferred_time, context)
            VALUES (?, ?, ?, ?)
        ''', (pattern, 1, preferred_time, context))

    conn.commit()
    conn.close()
    print(f"[PATTERN] Logged user pattern: {pattern}")

def save_preference(category, preference, confidence=0.8):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM preferences WHERE category = ?', (category,))
    row = cursor.fetchone()

    if row:
        cursor.execute('''
            UPDATE preferences 
            SET preference = ?, confidence = ?, last_updated = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (preference, confidence, row[0]))
    else:
        cursor.execute('''
            INSERT INTO preferences (category, preference, confidence)
            VALUES (?, ?, ?)
        ''', (category, preference, confidence))

    conn.commit()
    conn.close()
    print(f"[PREFERENCE] {category}: {preference} (confidence: {confidence})")

def get_recent_actions(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT timestamp, action, result, success 
        FROM action_log 
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_user_patterns():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT pattern, frequency, preferred_time, context 
        FROM user_profile 
        ORDER BY frequency DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows