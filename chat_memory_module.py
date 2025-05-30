#chat_memory_module.py

import sqlite3
import datetime

DB_NAME = "siriraj_memory.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_query TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            voice_sample BLOB, -- To store a voice sample if needed for recognition
            preferred_language TEXT DEFAULT 'en',
            automation_permission BOOLEAN DEFAULT FALSE
        )
    ''')
    conn.commit()
    conn.close()

def save_chat(user_query, ai_response):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (user_query, ai_response) VALUES (?, ?)", (user_query, ai_response))
    conn.commit()
    conn.close()

def get_chat_history(limit=10):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Fetching in reverse chronological order and then reversing to get chronological
    cursor.execute("SELECT user_query, ai_response FROM chat_history ORDER BY timestamp DESC LIMIT ?", (limit,))
    history = cursor.fetchall()
    conn.close()
    return history[::-1] # Return in chronological order (oldest to newest)

def get_user_name_from_voice_sample(voice_sample_data):
    # This is a highly complex feature requiring advanced voice recognition/speaker diarization.
    # It would involve:
    # 1. Training a model on known user voice samples.
    # 2. Extracting features from the incoming voice_sample_data.
    # 3. Comparing features to identify the speaker.
    # For a practical implementation, you might start with a simpler approach:
    # - Users register their voice and name once.
    # - You map a unique voice print/ID to a user's name.
    print("Chat Memory: User voice recognition is an advanced feature and currently a placeholder.")
    return "Sir" # Default for now

def set_user_automation_permission(user_name, permission):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Insert or update the user's permission
    cursor.execute("INSERT OR REPLACE INTO user_profiles (name, automation_permission) VALUES (?, ?)", (user_name, permission))
    conn.commit()
    conn.close()
    print(f"Chat Memory: Automation permission for {user_name} set to {permission}")


def get_user_automation_permission(user_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT automation_permission FROM user_profiles WHERE name = ?", (user_name,))
    result = cursor.fetchone()
    conn.close()
    # If user exists, return their permission; otherwise, default to False
    return bool(result[0]) if result else False

# Example of how to add a user initially (e.g., on first run or registration)
def add_or_update_user(name, initial_permission=False):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO user_profiles (name, automation_permission) VALUES (?, ?)", (name, initial_permission))
    conn.commit()
    conn.close()
