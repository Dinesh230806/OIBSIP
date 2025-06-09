import tkinter as tk
from tkinter import ttk
from typing import Dict, Optional
from datetime import datetime
from utils.icon_manager import IconManager


class CurrentWeather(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.current_icons = {}
        self.create_widgets()
        self.apply_styles()
        self.set_empty_state()

    def create_widgets(self):
        self.container = ttk.Frame(self, style='Card.TFrame')
        self.container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Top section: icon and temperature
        top_frame = ttk.Frame(self.container)
        top_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.icon_label = ttk.Label(top_frame)
        self.icon_label.pack(side=tk.LEFT, padx=10)

        info_frame = ttk.Frame(top_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.temp_var = tk.StringVar()
        temp_label = ttk.Label(info_frame, textvariable=self.temp_var, font=('Arial', 48, 'bold'), style='Temp.TLabel')
        temp_label.pack(anchor=tk.W)

        self.desc_var = tk.StringVar()
        desc_label = ttk.Label(info_frame, textvariable=self.desc_var, font=('Arial', 14), style='Desc.TLabel')
        desc_label.pack(anchor=tk.W)

        loc_time_frame = ttk.Frame(info_frame)
        loc_time_frame.pack(fill=tk.X, pady=(5, 0))

        self.location_var = tk.StringVar()
        location_label = ttk.Label(loc_time_frame, textvariable=self.location_var, font=('Arial', 10), style='Location.TLabel')
        location_label.pack(side=tk.LEFT, anchor=tk.W)

        self.time_var = tk.StringVar()
        time_label = ttk.Label(loc_time_frame, textvariable=self.time_var, font=('Arial', 8), style='Time.TLabel')
        time_label.pack(side=tk.RIGHT, anchor=tk.E)

        # Bottom section: details
        details_frame = ttk.Frame(self.container)
        details_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.detail_vars = {
            'feels_like': tk.StringVar(),
            'humidity': tk.StringVar(),
            'wind': tk.StringVar(),
            'pressure': tk.StringVar(),
            'visibility': tk.StringVar(),
            'sunrise': tk.StringVar(),
            'sunset': tk.StringVar(),
            'clouds': tk.StringVar()
        }

        left_col = ttk.Frame(details_frame)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_col = ttk.Frame(details_frame)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        details = [
            ('feels_like', left_col),
            ('humidity', left_col),
            ('wind', left_col),
            ('pressure', left_col),
            ('visibility', right_col),
            ('clouds', right_col),
            ('sunrise', right_col),
            ('sunset', right_col)
        ]

        for key, parent in details:
            ttk.Label(parent, textvariable=self.detail_vars[key], font=('Arial', 9), style='Detail.TLabel').pack(anchor=tk.W, pady=1)

    def apply_styles(self):
        style = ttk.Style()

        style.configure('Card.TFrame', background='#ffffff', borderwidth=1, relief='solid', padding=5)
        style.configure('Temp.TLabel', foreground='#333333', background='#ffffff')
        style.configure('Desc.TLabel', foreground='#555555', background='#ffffff')
        style.configure('Location.TLabel', foreground='#444444', background='#ffffff')
        style.configure('Time.TLabel', foreground='#888888', background='#ffffff')
        style.configure('Detail.TLabel', foreground='#555555', background='#ffffff')

    def set_empty_state(self):
        self.temp_var.set("--°")
        self.desc_var.set("No data available")
        self.location_var.set("Unknown location")
        self.time_var.set("")

        self.detail_vars['feels_like'].set("Feels like: --")
        self.detail_vars['humidity'].set("Humidity: --%")
        self.detail_vars['wind'].set("Wind: --")
        self.detail_vars['pressure'].set("Pressure: -- hPa")
        self.detail_vars['visibility'].set("Visibility: --")
        self.detail_vars['clouds'].set("Clouds: --%")
        self.detail_vars['sunrise'].set("Sunrise: --:--")
        self.detail_vars['sunset'].set("Sunset: --:--")

    def set_loading_state(self):
        """Show loading text while data is being fetched"""
        self.temp_var.set("Loading...")
        self.desc_var.set("Please wait")
        self.location_var.set("")
        self.time_var.set("")
        for key in self.detail_vars:
            self.detail_vars[key].set("")

    def update_data(self, weather_data: Optional[Dict], units: str = "metric"):
        if not weather_data:
            self.set_empty_state()
            return

        try:
            main = weather_data['main']
            weather = weather_data['weather'][0]
            sys = weather_data.get('sys', {})
            wind = weather_data.get('wind', {})
            clouds = weather_data.get('clouds', {})
            visibility = weather_data.get('visibility', 0)

            self.temp_var.set(f"{round(main['temp'])}°")
            self.desc_var.set(weather['description'].title())
            self.location_var.set(f"{weather_data['name']}, {sys.get('country', '')}")
            self.time_var.set(f"Updated: {datetime.now().strftime('%H:%M')}")

            icon_code = weather['icon']
            icon = IconManager.get_icon_image(icon_code, size=(80, 80))
            if icon:
                self.current_icons['weather'] = icon
                self.icon_label.configure(image=icon)

            wind_speed = round(wind.get('speed', 0), 1)
            wind_unit = "m/s" if units == "metric" else "mph"

            if visibility == 10000:
                visibility_str = "10+ km"
            elif visibility > 0:
                if units == "imperial":
                    vis_mi = round(visibility / 1609.34, 1)
                    visibility_str = f"{vis_mi} mi"
                else:
                    vis_km = round(visibility / 1000, 1)
                    visibility_str = f"{vis_km} km"
            else:
                visibility_str = "--"

            self.detail_vars['feels_like'].set(f"Feels like: {round(main['feels_like'])}°")
            self.detail_vars['humidity'].set(f"Humidity: {main['humidity']}%")
            self.detail_vars['wind'].set(f"Wind: {wind_speed} {wind_unit}")
            self.detail_vars['pressure'].set(f"Pressure: {main['pressure']} hPa")
            self.detail_vars['visibility'].set(f"Visibility: {visibility_str}")
            self.detail_vars['clouds'].set(f"Clouds: {clouds.get('all', '--')}%")

            if 'sunrise' in sys and 'sunset' in sys:
                sunrise = datetime.fromtimestamp(sys['sunrise']).strftime('%H:%M')
                sunset = datetime.fromtimestamp(sys['sunset']).strftime('%H:%M')
                self.detail_vars['sunrise'].set(f"Sunrise: {sunrise}")
                self.detail_vars['sunset'].set(f"Sunset: {sunset}")
            else:
                self.detail_vars['sunrise'].set("Sunrise: --:--")
                self.detail_vars['sunset'].set("Sunset: --:--")

        except Exception as e:
            print(f"[Error] Failed to update weather data: {e}")
            self.set_empty_state()
            self.desc_var.set("Data format error")
