# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk
# from utils.icon_manager import IconManager
# from datetime import datetime


# class ForecastDisplay(ttk.Frame):
#     """Displays 5-day weather forecast with icons and details"""

#     def __init__(self, parent):
#         super().__init__(parent, padding=(10, 5), style='Card.TFrame')
#         self.icons = {}  # Prevent garbage collection of icons
#         self.forecast_widgets = []  # Track widgets if needed (not strictly necessary here)

#         # Title label
#         ttk.Label(
#             self,
#             text="5-Day Forecast",
#             font=('Helvetica', 12, 'bold')
#         ).grid(row=0, column=0, columnspan=5, pady=(0, 10))

#         # Initialize container for each day's info
#         self.day_frames = []
#         self.day_labels = {
#             'date': [],
#             'icon': [],
#             'temp': [],
#             'description': []
#         }

#         for i in range(5):
#             day_frame = ttk.Frame(self)
#             day_frame.grid(row=1, column=i, padx=5, sticky=tk.N)

#             date_label = ttk.Label(day_frame, font=('Helvetica', 10, 'bold'))
#             date_label.pack(pady=(0, 2))

#             icon_label = ttk.Label(day_frame)
#             icon_label.pack(pady=(0, 2))

#             temp_label = ttk.Label(day_frame, font=('Helvetica', 10))
#             temp_label.pack(pady=(0, 2))

#             desc_label = ttk.Label(day_frame, font=('Helvetica', 9), wraplength=100, justify="center")
#             desc_label.pack(pady=(0, 2))

#             self.day_frames.append(day_frame)
#             self.day_labels['date'].append(date_label)
#             self.day_labels['icon'].append(icon_label)
#             self.day_labels['temp'].append(temp_label)
#             self.day_labels['description'].append(desc_label)

#     def update_forecast(self, forecast_data, units='metric'):
#         """Update display with new forecast data"""
#         try:
#             if not forecast_data or len(forecast_data) < 8:
#                 raise ValueError("Insufficient forecast data.")

#             daily_data = []
#             seen_dates = set()

#             for item in forecast_data:
#                 date_key = item['dt_txt'].split(" ")[0]
#                 if date_key not in seen_dates:
#                     seen_dates.add(date_key)
#                     daily_data.append({
#                         'date': self._format_date(item['dt_txt']),
#                         'icon': item['weather'][0]['icon'],
#                         'temp': f"{round(item['main']['temp'])}°{'C' if units == 'metric' else 'F'}",
#                         'description': item['weather'][0]['description'].title()
#                     })
#                 if len(daily_data) == 5:
#                     break

#             for i in range(5):
#                 if i < len(daily_data):
#                     day = daily_data[i]
#                     self.day_labels['date'][i].config(text=day['date'])
#                     self.day_labels['temp'][i].config(text=day['temp'])
#                     self.day_labels['description'][i].config(text=day['description'])

#                     icon_img = IconManager.get_icon_image(day['icon'], size=(48, 48))
#                     if icon_img:
#                         self.icons[f"day_{i}"] = icon_img
#                         self.day_labels['icon'][i].config(image=icon_img)
#                 else:
#                     self.day_labels['date'][i].config(text="")
#                     self.day_labels['temp'][i].config(text="")
#                     self.day_labels['description'][i].config(text="")
#                     self.day_labels['icon'][i].config(image="")
#                     if f"day_{i}" in self.icons:
#                         del self.icons[f"day_{i}"]

#         except Exception as e:
#             print(f"[Forecast Error] {e}")

#     def update_data(self, forecast_data, units='metric'):
#         """Alias to match expected method name used in the app"""
#         self.update_forecast(forecast_data, units)

#     def clear_data(self):
#         """Clear all forecast display data"""
#         for i in range(5):
#             self.day_labels['date'][i].config(text="")
#             self.day_labels['temp'][i].config(text="")
#             self.day_labels['description'][i].config(text="")
#             self.day_labels['icon'][i].config(image="")
#         self.icons.clear()

#     def _format_date(self, date_str):
#         """Convert API date string to readable format"""
#         try:
#             dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
#             return dt.strftime("%a\n%b %d")
#         except Exception as e:
#             print(f"[Date Parsing Error] {e}")
#             return date_str



import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from utils.icon_manager import IconManager
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ForecastDisplay(ttk.Frame):
    """Displays 5-day weather forecast with icons and details"""

    def __init__(self, parent):
        super().__init__(parent, padding=(10, 5), style='Card.TFrame')
        self.icons = {}  # Prevent garbage collection of icons
        self.forecast_widgets = []  # Track widgets if needed (not strictly necessary here)

        # Title label
        ttk.Label(
            self,
            text="5-Day Forecast",
            font=('Helvetica', 12, 'bold')
        ).grid(row=0, column=0, columnspan=5, pady=(0, 10))

        # Initialize container for each day's info
        self.day_frames = []
        self.day_labels = {
            'date': [],
            'icon': [],
            'temp': [],
            'description': []
        }

        for i in range(5):
            day_frame = ttk.Frame(self)
            day_frame.grid(row=1, column=i, padx=5, sticky=tk.N)

            date_label = ttk.Label(day_frame, font=('Helvetica', 10, 'bold'))
            date_label.pack(pady=(0, 2))

            icon_label = ttk.Label(day_frame)
            icon_label.pack(pady=(0, 2))

            temp_label = ttk.Label(day_frame, font=('Helvetica', 10), justify="center")
            temp_label.pack(pady=(0, 2))

            desc_label = ttk.Label(day_frame, font=('Helvetica', 9), wraplength=100, justify="center")
            desc_label.pack(pady=(0, 2))

            self.day_frames.append(day_frame)
            self.day_labels['date'].append(date_label)
            self.day_labels['icon'].append(icon_label)
            self.day_labels['temp'].append(temp_label)
            self.day_labels['description'].append(desc_label)

    def update_forecast(self, forecast_data, units='metric'):
        """Update display with new forecast data"""
        try:
            forecast_list = forecast_data.get('list', []) if isinstance(forecast_data, dict) else forecast_data
            if not forecast_list or len(forecast_list) < 8:
                raise ValueError("Insufficient forecast data.")

            daily_data = []
            seen_dates = set()

            for item in forecast_list:
                date_key = item['dt_txt'].split(" ")[0]
                if date_key not in seen_dates:
                    seen_dates.add(date_key)
                    daily_data.append({
                        'date': self._format_date(item['dt_txt']),
                        'icon': item['weather'][0]['icon'],
                        'temp': f"{round(item['main']['temp'])}°{'C' if units == 'metric' else 'F'}",
                        'description': item['weather'][0]['description'].title()
                    })
                if len(daily_data) == 5:
                    break

            for i in range(5):
                if i < len(daily_data):
                    day = daily_data[i]
                    self.day_labels['date'][i].config(text=day['date'])
                    self.day_labels['temp'][i].config(text=day['temp'])
                    self.day_labels['description'][i].config(text=day['description'])

                    icon_img = IconManager.get_icon_image(day['icon'], size=(48, 48))
                    if icon_img:
                        self.icons[f"day_{i}"] = icon_img
                        self.day_labels['icon'][i].config(image=icon_img)
                else:
                    self.day_labels['date'][i].config(text="")
                    self.day_labels['temp'][i].config(text="")
                    self.day_labels['description'][i].config(text="")
                    self.day_labels['icon'][i].config(image="")
                    if f"day_{i}" in self.icons:
                        del self.icons[f"day_{i}"]

        except Exception as e:
            logger.error(f"[Forecast Error] {e}")
            self.clear_data()

    def update_data(self, forecast_data, units='metric'):
        """Alias to match expected method name used in the app"""
        self.update_forecast(forecast_data, units)

    def clear_data(self):
        """Clear all forecast display data"""
        for i in range(5):
            self.day_labels['date'][i].config(text="")
            self.day_labels['temp'][i].config(text="")
            self.day_labels['description'][i].config(text="")
            self.day_labels['icon'][i].config(image="")
        self.icons.clear()

    def _format_date(self, date_str):
        """Convert API date string to readable format"""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%a\n%b %d")
        except Exception as e:
            logger.error(f"[Date Parsing Error] {e}")
            return date_str
