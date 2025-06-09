import matplotlib.pyplot as plt
from datetime import datetime

def plot_bmi_history(records, username):
    if not records:
        print("No BMI history to plot.")
        return

    dates = [datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S') for record in records]
    bmi_values = [record[3] for record in records]
    categories = [record[4] for record in records]

    color_map = {
        "Underweight": "blue",
        "Normal": "green",
        "Overweight": "orange",
        "Obese": "red"
    }
    colors = [color_map.get(cat, "gray") for cat in categories]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, bmi_values, linestyle='--', marker='o', color='black', label="BMI")
    plt.scatter(dates, bmi_values, c=colors, s=100, edgecolors='k', label="Categories")
    plt.axhline(18.5, color='blue', linestyle='dotted', label="18.5 (Underweight)")
    plt.axhline(24.9, color='green', linestyle='dotted', label="24.9 (Normal)")
    plt.axhline(29.9, color='orange', linestyle='dotted', label="29.9 (Overweight)")

    plt.title(f"BMI History for {username}")
    plt.xlabel("Date")
    plt.ylabel("BMI Value")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()









