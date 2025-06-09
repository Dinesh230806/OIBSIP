import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip

# Function to calculate strength
def get_strength(pw):
    length = len(pw)
    has_upper = any(c.isupper() for c in pw)
    has_lower = any(c.islower() for c in pw)
    has_digit = any(c.isdigit() for c in pw)
    has_symbol = any(c in string.punctuation for c in pw)

    score = sum([has_upper, has_lower, has_digit, has_symbol])
    if length < 6 or score <= 2:
        return "Weak", "red"
    elif 6 <= length <= 10 and score >= 3:
        return "Medium", "orange"
    else:
        return "Strong", "green"

def generate_password():
    try:
        length = int(length_entry.get())
        exclude = exclude_entry.get()
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
        return

    chars = ""
    if var_upper.get():
        chars += string.ascii_uppercase
    if var_lower.get():
        chars += string.ascii_lowercase
    if var_digits.get():
        chars += string.digits
    if var_symbols.get():
        chars += string.punctuation

    for c in exclude:
        chars = chars.replace(c, "")

    if not chars:
        messagebox.showwarning("Warning", "No character types selected.")
        return

    password = ''.join(random.choice(chars) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

    strength, color = get_strength(password)
    strength_label.config(text=f"Strength: {strength}", fg=color)

def copy_password():
    pw = password_entry.get()
    if pw:
        pyperclip.copy(pw)
        messagebox.showinfo("Copied", "Password copied to clipboard.")

def save_password():
    pw = password_entry.get()
    if pw:
        with open("passwords.txt", "a") as file:
            file.write(pw + "\n")
        messagebox.showinfo("Saved", "Password saved to passwords.txt")

# GUI Setup
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("400x450")
root.config(padx=20, pady=20)

tk.Label(root, text="Password Length:").pack()
length_entry = tk.Entry(root)
length_entry.insert(0, "12")
length_entry.pack()

tk.Label(root, text="Exclude Characters (Optional):").pack()
exclude_entry = tk.Entry(root)
exclude_entry.pack()

# Centered options
tk.Label(root, text="Include:").pack(pady=(10, 0))
checkbox_frame = tk.Frame(root)
checkbox_frame.pack(pady=5)

var_upper = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=False)

tk.Checkbutton(checkbox_frame, text="Uppercase Letters", variable=var_upper).grid(row=0, column=0, padx=10, pady=5)
tk.Checkbutton(checkbox_frame, text="Lowercase Letters", variable=var_lower).grid(row=0, column=1, padx=10, pady=5)
tk.Checkbutton(checkbox_frame, text="Numbers", variable=var_digits).grid(row=1, column=0, padx=10, pady=5)
tk.Checkbutton(checkbox_frame, text="Symbols", variable=var_symbols).grid(row=1, column=1, padx=10, pady=5)

# Buttons and Output
tk.Button(root, text="Generate Password", command=generate_password, bg="#007acc", fg="white").pack(pady=10)
password_entry = tk.Entry(root, font=("Arial", 14), justify="center")
password_entry.pack()

strength_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
strength_label.pack()

tk.Button(root, text="Copy to Clipboard", command=copy_password).pack(pady=5)
tk.Button(root, text="Save Password", command=save_password).pack(pady=5)

root.mainloop()
