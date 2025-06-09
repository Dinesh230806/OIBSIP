import sqlite3
from hashlib import sha256
import threading
import os
from datetime import datetime

class Database:
    def __init__(self, db_name='chat_app.db'):
        self.local = threading.local()
        self.db_name = db_name
        self.print_db_path()
        self.create_tables()

    def print_db_path(self):
        """Print the absolute path of the database for debugging."""
        print(f"📂 Database location: {os.path.abspath(self.db_name)}")

    def get_conn(self):
        """Get or create a thread-local SQLite connection."""
        if not hasattr(self.local, 'conn'):
            try:
                self.local.conn = sqlite3.connect(self.db_name, check_same_thread=False)
                self.local.conn.row_factory = sqlite3.Row
                self.local.conn.execute("PRAGMA journal_mode=WAL")
                self.local.conn.execute("PRAGMA foreign_keys=ON")
            except sqlite3.Error as e:
                print(f"🚨 Database connection failed: {e}")
                raise
        return self.local.conn

    def close_conn(self):
        """Close the thread-local connection if it exists."""
        if hasattr(self.local, 'conn'):
            try:
                self.local.conn.close()
                print("🛑 Database connection closed.")
            except sqlite3.Error as e:
                print(f"🚨 Error closing connection: {e}")
            finally:
                del self.local.conn

    def create_tables(self):
        """Create required tables if they do not exist."""
        try:
            with self.get_conn() as conn:
                conn.executescript('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    );

                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        room TEXT NOT NULL,
                        username TEXT NOT NULL,
                        message TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(username) REFERENCES users(username)
                    );

                    CREATE INDEX IF NOT EXISTS idx_messages_room ON messages(room);
                    CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
                ''')
        except sqlite3.Error as e:
            print(f"🚨 Table creation failed: {e}")
            raise

    def hash_password(self, password):
        """Hash a plain-text password."""
        return sha256(password.encode()).hexdigest()

    def store_message(self, room, username, message):
        """Store a message in the database."""
        try:
            with self.get_conn() as conn:
                conn.execute(
                    "INSERT INTO messages (room, username, message) VALUES (?, ?, ?)",
                    (room, username, message)
                )
            print(f"💾 Message saved: {username}@{room} → {message[:50]}...")
            return True
        except sqlite3.Error as e:
            print(f"🚨 Error saving message: {e}")
            return False

    def get_messages(self, room, limit=100):
        """Retrieve the last `limit` messages from a given room."""
        try:
            conn = self.get_conn()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT username, message, timestamp
                FROM messages
                WHERE room = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (room, limit))

            results = []
            for row in cursor.fetchall():
                timestamp = row['timestamp']
                if isinstance(timestamp, str):
                    try:
                        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        pass
                formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S") if isinstance(timestamp, datetime) else timestamp
                results.append(f"[{formatted_time}] {row['username']}: {row['message']}")
            return results[::-1]
        except sqlite3.Error as e:
            print(f"🚨 Error retrieving messages: {e}")
            return []

    def register_user(self, username, password):
        """Register a new user with a hashed password."""
        try:
            with self.get_conn() as conn:
                conn.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, self.hash_password(password))
                )
            print(f"✅ User registered: {username}")
            return True
        except sqlite3.IntegrityError:
            print(f"⚠️ Username already exists: {username}")
            return False
        except sqlite3.Error as e:
            print(f"🚨 Error registering user: {e}")
            return False

    def validate_user(self, username, password):
        """Validate a username and password combination."""
        try:
            conn = self.get_conn()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM users WHERE username = ? AND password = ?",
                (username, self.hash_password(password))
            )
            is_valid = cursor.fetchone() is not None
            print(f"{'✅' if is_valid else '❌'} Login attempt: {username}")
            return is_valid
        except sqlite3.Error as e:
            print(f"🚨 Error validating user: {e}")
            return False

import sqlite3
from hashlib import sha256
import threading
import os
from datetime import datetime

class Database:
    def __init__(self, db_name='chat_app.db'):
        self.local = threading.local()
        self.db_name = db_name
        self.print_db_path()
        self.create_tables()

    def print_db_path(self):
        """Print the absolute path of the database for debugging."""
        print(f"📂 Database location: {os.path.abspath(self.db_name)}")

    def get_conn(self):
        """Get or create a thread-local SQLite connection."""
        if not hasattr(self.local, 'conn'):
            try:
                self.local.conn = sqlite3.connect(self.db_name, check_same_thread=False)
                self.local.conn.row_factory = sqlite3.Row
                self.local.conn.execute("PRAGMA journal_mode=WAL")
                self.local.conn.execute("PRAGMA foreign_keys=ON")
            except sqlite3.Error as e:
                print(f"🚨 Database connection failed: {e}")
                raise
        return self.local.conn

    def close_conn(self):
        """Close the thread-local connection if it exists."""
        if hasattr(self.local, 'conn'):
            try:
                self.local.conn.close()
                print("🛑 Database connection closed.")
            except sqlite3.Error as e:
                print(f"🚨 Error closing connection: {e}")
            finally:
                del self.local.conn

    def create_tables(self):
        """Create required tables if they do not exist."""
        try:
            with self.get_conn() as conn:
                conn.executescript('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    );

                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        room TEXT NOT NULL,
                        username TEXT NOT NULL,
                        message TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(username) REFERENCES users(username)
                    );

                    CREATE INDEX IF NOT EXISTS idx_messages_room ON messages(room);
                    CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
                ''')
        except sqlite3.Error as e:
            print(f"🚨 Table creation failed: {e}")
            raise

    def hash_password(self, password):
        """Hash a plain-text password."""
        return sha256(password.encode()).hexdigest()

    def store_message(self, room, username, message):
        """Store a message in the database."""
        try:
            with self.get_conn() as conn:
                conn.execute(
                    "INSERT INTO messages (room, username, message) VALUES (?, ?, ?)",
                    (room, username, message)
                )
            print(f"💾 Message saved: {username}@{room} → {message[:50]}...")
            return True
        except sqlite3.Error as e:
            print(f"🚨 Error saving message: {e}")
            return False

    def get_messages(self, room, limit=100):
        """Retrieve the last `limit` messages from a given room."""
        try:
            conn = self.get_conn()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT username, message, timestamp
                FROM messages
                WHERE room = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (room, limit))

            results = []
            for row in cursor.fetchall():
                timestamp = row['timestamp']
                if isinstance(timestamp, str):
                    try:
                        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        pass
                formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S") if isinstance(timestamp, datetime) else timestamp
                results.append(f"[{formatted_time}] {row['username']}: {row['message']}")
            return results[::-1]
        except sqlite3.Error as e:
            print(f"🚨 Error retrieving messages: {e}")
            return []


    def authenticate_user(self, username, password):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return cursor.fetchone() is not None

    def add_user(self, username, password):
        conn = self.get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


    def register_user(self, username, password):
        """Register a new user with a hashed password."""
        try:
            with self.get_conn() as conn:
                conn.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, self.hash_password(password))
                )
            print(f"✅ User registered: {username}")
            return True
        except sqlite3.IntegrityError:
            print(f"⚠️ Username already exists: {username}")
            return False
        except sqlite3.Error as e:
            print(f"🚨 Error registering user: {e}")
            return False

    def validate_user(self, username, password):
        """Validate a username and password combination."""
        try:
            conn = self.get_conn()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM users WHERE username = ? AND password = ?",
                (username, self.hash_password(password))
            )
            is_valid = cursor.fetchone() is not None
            print(f"{'✅' if is_valid else '❌'} Login attempt: {username}")
            return is_valid
        except sqlite3.Error as e:
            print(f"🚨 Error validating user: {e}")
            return False
