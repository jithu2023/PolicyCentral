# backend/database.py
import sqlite3
import json
from datetime import datetime

DB_PATH = "users.db"

def init_db():
    """Initialize database tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE,
            name TEXT,
            age INTEGER,
            lifestyle TEXT,
            conditions TEXT,
            income TEXT,
            city TEXT,
            recommended_policy TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database initialized")

def save_profile(session_id: str, profile: dict):
    """Save or update user profile"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    conditions_json = json.dumps(profile.get('conditions', []))
    
    cursor.execute("""
        INSERT OR REPLACE INTO user_profiles 
        (session_id, name, age, lifestyle, conditions, income, city, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session_id,
        profile.get('name'),
        profile.get('age'),
        profile.get('lifestyle'),
        conditions_json,
        profile.get('income'),
        profile.get('city'),
        datetime.now()
    ))
    
    conn.commit()
    conn.close()

def get_profile(session_id: str):
    """Get user profile by session_id"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profiles WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'session_id': row[1],
            'name': row[2],
            'age': row[3],
            'lifestyle': row[4],
            'conditions': json.loads(row[5]),
            'income': row[6],
            'city': row[7],
            'recommended_policy': row[8],
            'created_at': row[9],
            'updated_at': row[10]
        }
    return None

def update_recommended_policy(session_id: str, policy_name: str):
    """Update the recommended policy for a user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE user_profiles 
        SET recommended_policy = ?, updated_at = ?
        WHERE session_id = ?
    """, (policy_name, datetime.now(), session_id))
    conn.commit()
    conn.close()