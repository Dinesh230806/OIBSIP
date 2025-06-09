import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import font as tkfont
from PIL import Image, ImageTk
import os
import base64
import io
import threading
import pystray
from pystray import MenuItem as item
from PIL import Image as PILImage

class ChatGUI(tk.Tk):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.title("Python Chat App")
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', padding=6)
        self.style.configure('TEntry', padding=6)
        
        # Create fonts
        self.message_font = tkfont.Font(family="Helvetica", size=12)
        self.username_font = tkfont.Font(family="Helvetica", size=10, weight="bold")
        
        # Setup authentication frame
        self.auth_frame = ttk.Frame(self)
        self.setup_auth_ui()
        self.auth_frame.pack(fill=tk.BOTH, expand=True)
        
        # Setup chat frame (hidden initially)
        self.chat_frame = ttk.Frame(self)
        self.setup_chat_ui()
        
        # System tray icon
        self.tray_icon = None
        self.setup_tray_icon()

    def setup_auth_ui(self):
        """Setup authentication UI"""
        container = ttk.Frame(self.auth_frame)
        container.pack(expand=True, padx=50, pady=50)
        
        ttk.Label(container, text="Python Chat App", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(container, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(container)
        self.username_entry.grid(row=1, column=1, pady=5, sticky=tk.EW)
        
        ttk.Label(container, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(container, show="*")
        self.password_entry.grid(row=2, column=1, pady=5, sticky=tk.EW)
        
        button_frame = ttk.Frame(container)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Login", command=self.handle_login).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Register", command=self.handle_register).pack(side=tk.LEFT, padx=5)
        
        # Make the entry widgets expand with window
        container.columnconfigure(1, weight=1)

    def setup_chat_ui(self):
        """Setup the main chat interface"""
        # Left sidebar with rooms and users
        sidebar = ttk.Frame(self.chat_frame, width=150)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        ttk.Label(sidebar, text="Chat Rooms", style='Heading.TLabel').pack(pady=10)
        self.room_listbox = tk.Listbox(sidebar)
        self.room_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.room_listbox.bind('<<ListboxSelect>>', self.on_room_select)
        
        ttk.Label(sidebar, text="Online Users", style='Heading.TLabel').pack(pady=10)
        self.user_listbox = tk.Listbox(sidebar)
        self.user_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Main chat area
        main_area = ttk.Frame(self.chat_frame)
        main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Message display
        self.message_text = tk.Text(main_area, wrap=tk.WORD, state=tk.DISABLED)
        self.message_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Message input area
        input_frame = ttk.Frame(main_area)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.emoji_button = ttk.Button(input_frame, text="😊", command=self.show_emoji_picker)
        self.emoji_button.pack(side=tk.LEFT)
        
        self.attach_button = ttk.Button(input_frame, text="Attach", command=self.attach_file)
        self.attach_button.pack(side=tk.LEFT, padx=5)
        
        self.message_entry = ttk.Entry(input_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.message_entry.bind("<Return>", self.send_message)
        
        self.send_button = ttk.Button(input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

    def setup_tray_icon(self):
        """Setup system tray icon for notifications"""
        image = PILImage.new('RGB', (64, 64), 'white')
        menu = (item('Show', self.show_window), item('Exit', self.quit_app))
        self.tray_icon = pystray.Icon("chat_app", image, "Chat App", menu)
        
        # Start tray icon in a separate thread
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def show_window(self, icon, item):
        """Show the main window from tray icon"""
        self.deiconify()
        self.lift()

    def quit_app(self):
        """Quit the application"""
        self.destroy()
        os._exit(0)

    def handle_login(self):
        """Handle login button click"""
        self.authenticate('login')

    def handle_register(self):
        """Handle register button click"""
        self.authenticate('register')

    def authenticate(self, action):
        """Authenticate with server"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return
        
        success, response = self.client.connect(username, password, action)
        if success:
            self.auth_frame.pack_forget()
            self.chat_frame.pack(fill=tk.BOTH, expand=True)
            
            # Populate room list
            for room in response:
                self.room_listbox.insert(tk.END, room)
            
            # Join default room
            self.client.join_room('general')
        else:
            messagebox.showerror("Error", response)

    def send_message(self, event=None):
        """Send message to server"""
        message = self.message_entry.get()
        if message:
            self.client.send_message(message)
            self.message_entry.delete(0, tk.END)

    def display_message(self, message):
        """Display incoming message in the chat window"""
        self.message_text.config(state=tk.NORMAL)
        
        # Check if message contains an image
        if message.startswith('[IMAGE]'):
            img_data = message[7:]
            self.display_image(img_data)
        else:
            # Format regular message
            if ':' in message:
                username, msg_content = message.split(':', 1)
                self.message_text.insert(tk.END, username + ':', 'username')
                self.message_text.insert(tk.END, msg_content + '\n')
            else:
                self.message_text.insert(tk.END, message + '\n')
        
        self.message_text.config(state=tk.DISABLED)
        self.message_text.see(tk.END)
        
        # Show notification if window not focused
        if not self.focus_get():
            self.show_notification(message)

    def display_image(self, img_data):
        """Display base64 encoded image in chat"""
        try:
            img_bytes = base64.b64decode(img_data)
            img = Image.open(io.BytesIO(img_bytes))
            img.thumbnail((400, 400))
            
            photo = ImageTk.PhotoImage(img)
            self.message_text.image_create(tk.END, image=photo)
            self.message_text.insert(tk.END, '\n')
            
            # Keep reference to prevent garbage collection
            if not hasattr(self, 'image_references'):
                self.image_references = []
            self.image_references.append(photo)
        except Exception as e:
            self.message_text.insert(tk.END, f"[Failed to display image: {str(e)}]\n")

    def show_notification(self, message):
        """Show desktop notification"""
        if self.tray_icon:
            # Truncate long messages
            if len(message) > 50:
                message = message[:50] + "..."
            self.tray_icon.notify(message, "New Message")

    def update_message_history(self, messages):
        """Update chat with message history"""
        self.message_text.config(state=tk.NORMAL)
        self.message_text.delete(1.0, tk.END)
        
        for message in messages:
            self.display_message(message)
        
        self.message_text.config(state=tk.DISABLED)
        self.message_text.see(tk.END)

    def on_room_select(self, event):
        """Handle room selection change"""
        selection = self.room_listbox.curselection()
        if selection:
            room = self.room_listbox.get(selection[0])
            self.client.change_room(room)

    def show_emoji_picker(self):
        """Show emoji picker dialog"""
        emoji_window = tk.Toplevel(self)
        emoji_window.title("Select Emoji")
        
        # Sample emojis - in a real app you'd have a more comprehensive list
        emojis = ["😀", "😂", "😍", "😎", "👍", "👋", "❤️", "🔥"]
        
        for i, emoji in enumerate(emojis):
            btn = ttk.Button(emoji_window, text=emoji, 
                           command=lambda e=emoji: self.insert_emoji(e, emoji_window))
            btn.grid(row=i//5, column=i%5, padx=5, pady=5)

    def insert_emoji(self, emoji, window):
        """Insert selected emoji into message input"""
        self.message_entry.insert(tk.END, emoji)
        window.destroy()

    def attach_file(self):
        """Handle file attachment"""
        filepath = filedialog.askopenfilename(
            title="Select file to send",
            filetypes=[("Images", "*.jpg *.png *.gif"), ("All Files", "*.*")]
        )
        
        if filepath:
            try:
                with open(filepath, 'rb') as f:
                    file_data = f.read()
                
                # Convert to base64 for transmission
                encoded = base64.b64encode(file_data).decode('utf-8')
                self.client.send_message(f"[IMAGE]{encoded}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send file: {str(e)}")

    def on_close(self):
        """Handle window close event"""
        self.withdraw()  # Hide window instead of closing

    def quit_app(self):
        """Quit the application"""
        self.destroy()
        os._exit(0)