import tkinter as tk
from tkinter import ttk
from typing import Callable, List

class SearchPanel(ttk.Frame):
    def __init__(self, master, search_callback: Callable[[str], None], 
                 get_history_callback: Callable[[], List[str]], 
                 unit_callback: Callable[[str], None], **kwargs):
        super().__init__(master, **kwargs)
        self.search_callback = search_callback
        self.get_history_callback = get_history_callback
        self.unit_callback = unit_callback
        self.history_menu_visible = False

        self.create_widgets()
        self.setup_bindings()
        self.apply_styles()

    def create_widgets(self):
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_var, width=40, style="Search.TEntry")
        self.search_entry.grid(row=0, column=0, padx=(10, 0), pady=15, sticky="ew")

        self.search_button = ttk.Button(self, text="Search", command=self.search, style="Accent.TButton")
        self.search_button.grid(row=0, column=1, padx=(5, 0), pady=15)

        self.history_button = ttk.Button(self, text="⏷", command=self.toggle_history_menu, width=3, style="History.TButton")
        self.history_button.grid(row=0, column=2, padx=(5, 0), pady=15)

        self.history_menu = tk.Frame(self, bg="white", bd=1, relief="solid")
        self.history_menu.grid_columnconfigure(0, weight=1)
        self.history_menu.grid_propagate(False)
        self.history_menu.place_forget()

        self.autocomplete_window = tk.Toplevel(self)
        self.autocomplete_window.wm_overrideredirect(True)
        self.autocomplete_window.geometry("0x0")
        self.autocomplete_window.withdraw()

        self.autocomplete_list = tk.Listbox(
            self.autocomplete_window, height=5, bg="white", bd=0,
            highlightthickness=1, relief="solid", selectbackground="#0078D7",
            selectforeground="white", font=("Segoe UI", 10), width=30
        )
        self.autocomplete_list.pack(side="left", fill="both", expand=True)

        self.unit_var = tk.StringVar(value="C")
        self.unit_frame = tk.Frame(self, bg="white")
        self.unit_frame.grid(row=0, column=3, padx=(5, 10), pady=15, sticky="e")

        self.celsius_button = ttk.Radiobutton(
            self.unit_frame, text="°C", value="C", variable=self.unit_var,
            command=self.on_unit_change
        )
        self.celsius_button.pack(side="left", padx=2)

        self.fahrenheit_button = ttk.Radiobutton(
            self.unit_frame, text="°F", value="F", variable=self.unit_var,
            command=self.on_unit_change
        )
        self.fahrenheit_button.pack(side="left", padx=2)

    def setup_bindings(self):
        self.search_entry.bind("<KeyRelease>", self.on_keyrelease)
        self.search_entry.bind("<Return>", self.search)
        self.search_entry.bind("<FocusIn>", self.on_entry_focus)
        self.autocomplete_list.bind("<<ListboxSelect>>", self.on_autocomplete_select)
        self.search_entry.bind_all("<Button-1>", self.on_click_outside, add="+")

    def apply_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Search.TEntry", font=("Segoe UI", 11), padding=5)
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), foreground="white", background="#0078D7")
        style.map("Accent.TButton", background=[("active", "#005A9E")])
        style.configure("History.TButton", font=("Segoe UI", 10), padding=2)

    def search(self, event=None):
        text = self.search_var.get().strip()
        if text:
            self.search_callback(text)
            self.unit_callback(self.unit_var.get())
            self.hide_autocomplete()

    def on_unit_change(self):
        unit = self.unit_var.get()
        self.unit_callback(unit)

    def on_keyrelease(self, event):
        value = self.search_var.get().strip()
        if value:
            suggestions = self.get_suggestions(value)
            self.show_autocomplete(suggestions)
        else:
            self.hide_autocomplete()

    def on_entry_focus(self, event):
        self.search_entry.select_range(0, tk.END)

    def get_suggestions(self, text: str) -> List[str]:
        all_items = self.get_history_callback()
        return [item for item in all_items if text.lower() in item.lower()][:5]

    def show_autocomplete(self, suggestions: List[str]):
        if suggestions:
            self.autocomplete_list.delete(0, tk.END)
            for suggestion in suggestions:
                self.autocomplete_list.insert(tk.END, suggestion)

            x = self.search_entry.winfo_rootx()
            y = self.search_entry.winfo_rooty() + self.search_entry.winfo_height()
            width = self.search_entry.winfo_width()

            self.autocomplete_window.geometry(f"{width}x100+{x}+{y}")
            self.autocomplete_window.deiconify()
        else:
            self.hide_autocomplete()

    def hide_autocomplete(self):
        self.autocomplete_window.withdraw()

    def on_autocomplete_select(self, event):
        selection = self.autocomplete_list.curselection()
        if selection:
            value = self.autocomplete_list.get(selection[0])
            self.search_var.set(value)
            self.search()

    def toggle_history_menu(self):
        if self.history_menu_visible:
            self.hide_history_menu()
        else:
            self.show_history_menu()

    def show_history_menu(self):
        for widget in self.history_menu.winfo_children():
            widget.destroy()

        history = self.get_history_callback()
        for idx, item in enumerate(history[:5]):
            button = tk.Button(self.history_menu, text=item, bg="white", anchor="w", relief="flat",
                               command=lambda val=item: self.select_history(val), padx=10)
            button.grid(row=idx, column=0, sticky="ew")

        x = self.history_button.winfo_x()
        y = self.history_button.winfo_y() + self.history_button.winfo_height()

        self.history_menu.place(x=x, y=y, width=150)
        self.history_menu_visible = True

    def hide_history_menu(self):
        self.history_menu.place_forget()
        self.history_menu_visible = False

    def select_history(self, value: str):
        self.search_var.set(value)
        self.hide_history_menu()
        self.search()

    def on_click_outside(self, event):
        if not self.history_menu.winfo_containing(event.x_root, event.y_root):
            self.hide_history_menu()
        if not self.autocomplete_window.winfo_containing(event.x_root, event.y_root):
            self.hide_autocomplete()

    def set_location(self, location: str):
        self.search_var.set(location)
        self.search()

    def set_unit(self, unit: str):
        self.unit_var.set(unit)
        self.unit_callback(unit)

    def get_current_location(self):
        return self.search_var.get().strip()
