import tkinter as tk
from tkinter import ttk

class LocationDialog(tk.Toplevel):
    def __init__(self, parent, locations):
        super().__init__(parent)
        self.title("Select Location")
        self.selected_location = None
        
        ttk.Label(self, text="Multiple matches found:").pack(pady=10)
        
        for loc in locations:
            btn = ttk.Button(
                self,
                text=f"{loc['name']}, {loc.get('state', '')}, {loc['country']}",
                command=lambda l=loc: self.select_location(l)
            )
            btn.pack(fill=tk.X, padx=20, pady=2)
    
    def select_location(self, location):
        self.selected_location = location
        self.destroy()