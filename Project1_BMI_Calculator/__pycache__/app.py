import tkinter as tk
from tkinter import ttk, messagebox
from database import register_user, validate_login, save_bmi_record, get_bmi_history
from utils import calculate_bmi, classify_bmi, get_health_tip
from plotting import plot_bmi_history

current_user_id = None
current_username = ""

def login():
    global current_user_id, current_username
    username = login_username.get()
    password = login_password.get()
    user_id = validate_login(username, password)
    if user_id:
        current_user_id = user_id
        current_username = username
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        tab_control.select(bmi_tab)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def register():
    username = reg_username.get()
    password = reg_password.get()
    if register_user(username, password):
        messagebox.showinfo("Success", "Registration complete. You can now log in.")
        reg_username.delete(0, tk.END)
        reg_password.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Username already exists. Try a different one.")

def calculate_and_save_bmi():
    try:
        height = float(entry_height.get())
        weight = float(entry_weight.get())
        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)
        tip = get_health_tip(category)
        result_label.config(text=f"BMI: {bmi} ({category})")
        tip_label.config(text=f"Tip: {tip}")
        save_bmi_record(current_user_id, height, weight, bmi, category)
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter valid height and weight.")

def show_history():
    records = get_bmi_history(current_user_id)
    if not records:
        messagebox.showinfo("No Records", "No BMI history found.")
    else:
        plot_bmi_history(records, current_username)

root = tk.Tk()
root.title("BMI Tracker App")
root.geometry("600x400")

tab_control = ttk.Notebook(root)

login_tab = ttk.Frame(tab_control)
tab_control.add(login_tab, text="Login")
ttk.Label(login_tab, text="Username").pack(pady=5)
login_username = ttk.Entry(login_tab)
login_username.pack()
ttk.Label(login_tab, text="Password").pack(pady=5)
login_password = ttk.Entry(login_tab, show="*")
login_password.pack()
ttk.Button(login_tab, text="Login", command=login).pack(pady=10)

register_tab = ttk.Frame(tab_control)
tab_control.add(register_tab, text="Register")
ttk.Label(register_tab, text="New Username").pack(pady=5)
reg_username = ttk.Entry(register_tab)
reg_username.pack()
ttk.Label(register_tab, text="New Password").pack(pady=5)
reg_password = ttk.Entry(register_tab, show="*")
reg_password.pack()
ttk.Button(register_tab, text="Register", command=register).pack(pady=10)

bmi_tab = ttk.Frame(tab_control)
tab_control.add(bmi_tab, text="BMI Entry")
ttk.Label(bmi_tab, text="Height (cm)").pack(pady=5)
entry_height = ttk.Entry(bmi_tab)
entry_height.pack()
ttk.Label(bmi_tab, text="Weight (kg)").pack(pady=5)
entry_weight = ttk.Entry(bmi_tab)
entry_weight.pack()
ttk.Button(bmi_tab, text="Calculate & Save BMI", command=calculate_and_save_bmi).pack(pady=10)
result_label = ttk.Label(bmi_tab, text="")
result_label.pack()
tip_label = ttk.Label(bmi_tab, text="")
tip_label.pack()

history_tab = ttk.Frame(tab_control)
tab_control.add(history_tab, text="Dashboard")
ttk.Button(history_tab, text="Show BMI History Graph", command=show_history).pack(pady=20)

tab_control.pack(expand=1, fill="both")

root.mainloop()




