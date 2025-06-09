import socket
import threading
import json
from datetime import datetime
from database import Database
from encryption import EncryptionManager
from dotenv import load_dotenv
load_dotenv()  # Add at the top of server.py
class ChatServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server = None
        self.clients = {}  # {client_socket: {username: str, room: str, joined_at: str}}
        self.rooms = {'general': [], 'random': [], 'support': []}
        self.lock = threading.Lock()
        self.running = False
        self.db = Database()
        self.encryption = EncryptionManager()
        self.initialize_server()
        print(f"Server initialized on {host}:{port}")

    def initialize_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.settimeout(2)
        self.server.listen(5)

    def broadcast(self, room, message, sender=None):
        with self.lock:
            clients_in_room = list(self.rooms.get(room, []))
            encrypted_msg = self.encryption.encrypt(message)

            for client in clients_in_room:
                if client != sender:
                    try:
                        client.send(encrypted_msg)
                    except:
                        self.remove_client(client)

    def remove_client(self, client):
        with self.lock:
            if client not in self.clients:
                return

            user_info = self.clients[client]
            username = user_info['username']
            room = user_info['room']

            if room in self.rooms and client in self.rooms[room]:
                self.rooms[room].remove(client)
                self.broadcast(room, f"{username} left the chat")

            del self.clients[client]
            try:
                client.close()
            except:
                pass

    def handle_client(self, client, address):
        try:
            client.settimeout(30.0)
            auth_data = client.recv(4096).decode('utf-8')
            auth = json.loads(auth_data)

            username = auth.get('username', '').strip()
            password = auth.get('password', '')
            action = auth.get('action', '')

            if not username or not password or action not in ('register', 'login'):
                raise ValueError("Invalid authentication data")

            if action == 'register':
                success = self.db.register_user(username, password)
                message = "Registration successful" if success else "Username already exists"
            else:
                success = self.db.authenticate_user(username, password)
                message = "Login successful" if success else "Invalid credentials"

            if not success:
                client.send(json.dumps({'status': 'failed', 'message': message}).encode('utf-8'))
                client.close()
                return

            with self.lock:
                self.clients[client] = {'username': username, 'room': None, 'joined_at': datetime.now().isoformat()}

            client.send(json.dumps({'status': 'success', 'message': message, 'rooms': list(self.rooms)}).encode('utf-8'))

            room_data = client.recv(4096).decode('utf-8')
            room_choice = json.loads(room_data).get('room', 'general')
            if room_choice not in self.rooms:
                room_choice = 'general'

            with self.lock:
                self.clients[client]['room'] = room_choice
                self.rooms[room_choice].append(client)

            self.broadcast(room_choice, f"{username} joined the chat!", sender=client)

            history = self.db.get_messages(room_choice)
            client.send(json.dumps({'type': 'room_change', 'room': room_choice, 'history': history}).encode('utf-8'))

            client.settimeout(None)
            while self.running:
                try:
                    data = client.recv(4096)
                    if not data:
                        break

                    message = self.encryption.decrypt(data)
                    if not message:
                        continue

                    if message.startswith('/'):
                        self.handle_command(message, client)
                    else:
                        timestamp = datetime.now().strftime('%H:%M:%S')
                        full_msg = f"[{timestamp}] {username}: {message}"
                        self.db.store_message(room_choice, full_msg)
                        self.broadcast(room_choice, full_msg, sender=client)
                except (socket.timeout, json.JSONDecodeError, ConnectionError):
                    break
        except Exception as e:
            print(f"Client error ({address}): {e}")
        finally:
            self.remove_client(client)

    def handle_command(self, command, client):
        try:
            if not command.startswith('/'):
                return

            with self.lock:
                if client not in self.clients:
                    return
                username = self.clients[client]['username']
                current_room = self.clients[client]['room']

            if command.startswith('/join '):
                new_room = command.split(' ')[1]
                if new_room not in self.rooms:
                    return

                with self.lock:
                    if current_room == new_room:
                        return

                    self.rooms[current_room].remove(client)
                    self.rooms[new_room].append(client)
                    self.clients[client]['room'] = new_room

                history = self.db.get_messages(new_room)
                client.send(json.dumps({'type': 'room_change', 'room': new_room, 'history': history}).encode('utf-8'))

                self.broadcast(current_room, f"{username} left the room", client)
                self.broadcast(new_room, f"{username} joined the room", client)

            elif command == '/users':
                with self.lock:
                    room = self.clients[client]['room']
                    users = [self.clients[c]['username'] for c in self.rooms[room] if c in self.clients]
                client.send(self.encryption.encrypt(f"Users in room ({len(users)}): {', '.join(users)}"))
        except Exception as e:
            print(f"Command error: {e}")

    def start(self):
        self.running = True
        print(f"Chat server started on {self.host}:{self.port}")
        print(f"Available rooms: {', '.join(self.rooms)}")
        try:
            while self.running:
                try:
                    client, addr = self.server.accept()
                    print(f"Accepted connection from {addr}")
                    threading.Thread(target=self.handle_client, args=(client, addr), daemon=True).start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("Keyboard interrupt received. Shutting down server...")
        finally:
            self.shutdown()

    def shutdown(self):
        print("Shutting down server...")
        self.running = False
        with self.lock:
            for client in list(self.clients):
                try:
                    client.close()
                except:
                    pass
            self.clients.clear()
            for room in self.rooms:
                self.rooms[room].clear()

        if self.server:
            self.server.close()
    
        self.db.close_conn()  # ✅ Correctly closes the DB connection
        print("Server shutdown complete.")


if __name__ == "__main__":
    try:
        server = ChatServer()
        server.start()
    except Exception as e:
        print(f"Failed to start server: {e}")
