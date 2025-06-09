import socket
import threading
import json
import time
from encryption import EncryptionManager
from gui import ChatGUI

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.client = None
        self.encryption = EncryptionManager()
        self.gui = None
        self.username = None
        self.current_room = None
        self.running = False
        print(f"Client initialized, connecting to {host}:{port}")

    def initialize_socket(self):
        """Initialize a fresh socket connection"""
        if self.client:
            self.client.close()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(5)

    def connect(self, username, password, action):
        """Connect to server and authenticate with proper error handling"""
        try:
            self.initialize_socket()
            print(f"Attempting to connect to {self.host}:{self.port}...")
            self.client.connect((self.host, self.port))
            print("Connection established, authenticating...")

            auth_data = {
                'action': action,
                'username': username,
                'password': password
            }

            self.client.send(json.dumps(auth_data).encode('utf-8'))
            response = self.client.recv(4096)

            if not response:
                return False, "No response from server"

            response_data = json.loads(response.decode('utf-8'))

            if response_data.get('status') == 'success':
                self.username = username
                self.running = True
                return True, response_data.get('rooms', [])

            return False, response_data.get('message', 'Authentication failed')

        except socket.timeout:
            return False, "Connection timeout - server not responding"
        except ConnectionRefusedError:
            return False, "Connection refused - is the server running?"
        except Exception as e:
            return False, f"Connection error: {str(e)}"

    def join_room(self, room):
        """Join a chat room with error handling"""
        try:
            self.client.send(json.dumps({'room': room}).encode('utf-8'))
            self.current_room = room

            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            return True
        except Exception as e:
            print(f"Error joining room: {e}")
            if self.gui:
                self.gui.show_error(f"Failed to join room: {str(e)}")
            return False

    def receive_messages(self):
        """Receive and process messages from server"""
        while self.running:
            try:
                message = self.client.recv(4096)
                if not message:
                    print("Server closed connection")
                    self.running = False
                    break

                try:
                    decoded = json.loads(message.decode('utf-8'))
                    if decoded.get('type') == 'room_change':
                        self.current_room = decoded['room']
                        if self.gui:
                            self.gui.update_message_history(decoded.get('history', []))
                    continue
                except json.JSONDecodeError:
                    pass

                decrypted = self.encryption.decrypt(message)
                if self.gui:
                    self.gui.display_message(decrypted)

            except ConnectionResetError:
                print("Connection reset by server")
                self.running = False
                if self.gui:
                    self.gui.show_error("Connection lost with server")
                break
            except Exception as e:
                print(f"Error receiving message: {e}")
                if self.gui:
                    self.gui.show_error(f"Connection error: {str(e)}")
                break

    def send_message(self, message):
        """Send message to server with encryption"""
        if not message or not self.running:
            return False

        try:
            encrypted = self.encryption.encrypt(message)
            self.client.send(encrypted)
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            if self.gui:
                self.gui.show_error("Failed to send message")
            return False

    def change_room(self, room_name):
        """Change the chat room"""
        try:
            self.send({
                "type": "change_room",
                "room": room_name
            })
        except Exception as e:
            if self.gui:
                self.gui.show_error(f"Error changing room: {str(e)}")

    def send(self, data):
        """Send raw JSON data"""
        message = json.dumps(data).encode()
        self.client.send(message)

    def disconnect(self):
        """Cleanly disconnect from server"""
        self.running = False
        try:
            if self.client:
                self.client.close()
        except:
            pass
        finally:
            self.client = None

    def start_gui(self):
        """Start the GUI interface"""
        try:
            self.gui = ChatGUI(self)
            self.gui.mainloop()
        finally:
            self.disconnect()

if __name__ == "__main__":
    client = ChatClient()
    try:
        # First try to register
        print("Attempting to register...")
        success, message = client.connect("admin", "password123", "register")

        # If user exists, fallback to login
        if not success and "exists" in message.lower():
            print("User exists, attempting to login...")
            time.sleep(0.5)
            success, message = client.connect("admin", "password123", "login")

        print(f"Operation {'successful' if success else 'failed'}: {message}")

        if success:
            print("Starting GUI...")
            client.start_gui()

    except KeyboardInterrupt:
        print("\nClient shutting down...")
    finally:
        client.disconnect()
