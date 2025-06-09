import sqlite3
from datetime import datetime

def view_messages():
    db_path = "chat_app.db"  # Make sure this matches your actual DB path
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get last 10 messages
        cursor.execute("""
            SELECT username, message, room, timestamp 
            FROM messages 
            ORDER BY timestamp DESC 
            LIMIT 10
        """)
        
        print("\n=== Last 10 Chat Messages ===")
        for i, (user, msg, room, timestamp) in enumerate(cursor.fetchall(), 1):
            # Convert timestamp to readable format if needed
            if isinstance(timestamp, str):
                try:
                    timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    pass
            print(f"{i}. [{timestamp}] {user} ({room}): {msg}")
            
    except sqlite3.Error as e:
        print(f"\nError reading database: {e}")
        print("Possible causes:")
        print("- Database file not found")
        print("- No messages have been saved yet")
        print("- Database schema is different than expected")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    view_messages()
    input("\nPress Enter to exit...")