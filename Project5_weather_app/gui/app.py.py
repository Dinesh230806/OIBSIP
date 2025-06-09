# import tkinter as tk
# from tkinter import ttk, messagebox
# from typing import List

# # Import custom components
# from gui.components.search_panel import SearchPanel
# from gui.components.current_weather import CurrentWeather
# from gui.components.forecast import ForecastDisplay
# from utils.api_handler import APIHandler
# from config import Config


# class WeatherApp(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Advanced Weather App")
#         self.geometry("900x700")
#         self.minsize(800, 600)

#         # Initialize search history
#         self.search_history = []

#         # Configure styles
#         self.style = ttk.Style(self)
#         self.configure_styles()

#         # Create widgets
#         self.create_widgets()

#         # Load default location if available
#         default_location = getattr(Config, 'DEFAULT_LOCATION', None)
#         if default_location:
#             self.search_panel.set_location(default_location)
#             self.search_panel.search()

#     def configure_styles(self):
#         """Configure custom styles for the application"""
#         self.style.theme_use('clam')

#         # Frame styles
#         self.style.configure('TFrame', background='#f0f0f0')
#         self.style.configure('Card.TFrame',
#                              background='white',
#                              borderwidth=1,
#                              relief='groove',
#                              padding=10)

#         # Button styles
#         self.style.configure('Accent.TButton',
#                              foreground='white',
#                              background='#4285f4',
#                              font=('Arial', 10, 'bold'),
#                              padding=5)
#         self.style.map('Accent.TButton',
#                        background=[('active', '#3367d6')])

#         # Label styles
#         self.style.configure('Title.TLabel',
#                              font=('Arial', 12, 'bold'),
#                              foreground='#333333')

#         self.style.configure('Temp.TLabel',
#                              font=('Arial', 48, 'bold'),
#                              foreground='#222222')

#     def create_widgets(self):
#         """Create and arrange all widgets"""
#         # Main container
#         main_frame = ttk.Frame(self)
#         main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

#         # Search panel
#         self.search_panel = SearchPanel(
#             main_frame,
#             search_callback=self.handle_search,
#             get_history_callback=self.get_search_history,
#             unit_callback=self.handle_unit_change,
#             padding=10
#         )
#         self.search_panel.pack(fill=tk.X, pady=(0, 10))

#         # Current weather display
#         self.current_weather = CurrentWeather(main_frame)
#         self.current_weather.pack(fill=tk.BOTH, expand=True)

#         # Forecast display
#         forecast_label = ttk.Label(
#             main_frame,
#             text="5-Day Forecast",
#             style='Title.TLabel'
#         )
#         forecast_label.pack(pady=(10, 5))

#         self.forecast = ForecastDisplay(main_frame)
#         self.forecast.pack(fill=tk.BOTH, expand=True)

#     def handle_search(self, location: str):
#         """Handle search requests"""
#         if not location.strip():
#             messagebox.showwarning("Warning", "Location cannot be empty.")
#             return

#         try:
#             # Show loading state
#             self.current_weather.set_loading_state()
#             self.forecast.clear_data()

#             # First, get lat/lon for location string
#             location_results = APIHandler.get_location_results(location)

#             if not location_results:
#                 messagebox.showerror("Error", f"Location '{location}' not found.")
#                 self.current_weather.set_empty_state()
#                 self.forecast.clear_data()
#                 return

#             # Use first location result
#             lat = location_results[0]['lat']
#             lon = location_results[0]['lon']

#             units = self.get_current_units()

#             # Get current weather and forecast by lat, lon
#             current_data = APIHandler.get_current_weather(lat, lon, units)
#             forecast_data = APIHandler.get_forecast(lat, lon, units)

#             if current_data and forecast_data:
#                 # Update displays
#                 self.current_weather.update_data(current_data, units)
#                 self.forecast.update_data(forecast_data, units)

#                 # Add to search history
#                 if location not in self.search_history:
#                     self.search_history.append(location)
#             else:
#                 messagebox.showerror("Error", "Failed to fetch weather data.")
#                 self.current_weather.set_empty_state()
#                 self.forecast.clear_data()

#         except Exception as e:
#             messagebox.showerror("Error", f"An error occurred: {str(e)}")
#             self.current_weather.set_empty_state()
#             self.forecast.clear_data()

#     def handle_unit_change(self, unit: str):
#         """Handle unit changes (C/F)"""
#         current_location = self.search_panel.get_current_location()
#         if current_location:
#             self.handle_search(current_location)

#     def get_search_history(self) -> List[str]:
#         """Return search history (last 10 items, most recent first)"""
#         return self.search_history[-10:][::-1]

#     def get_current_units(self) -> str:
#         """Get current unit system (metric/imperial)"""
#         unit = getattr(self.search_panel, 'unit_var', None)
#         if unit:
#             return 'metric' if unit.get() == 'C' else 'imperial'
#         return 'metric'


# if __name__ == "__main__":
#     app = WeatherApp()
#     app.mainloop()



import tkinter as tk
from tkinter import ttk, messagebox
from typing import List

# Import custom components
from gui.components.search_panel import SearchPanel
from gui.components.current_weather import CurrentWeather
from gui.components.forecast import ForecastDisplay
from utils.api_handler import APIHandler
from config import Config


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Weather App")
        self.geometry("900x700")
        self.minsize(800, 600)

        # Initialize search history
        self.search_history = []

        # Configure styles
        self.style = ttk.Style(self)
        self.configure_styles()

        # Create widgets
        self.create_widgets()

        # Load default location if available
        default_location = getattr(Config, 'DEFAULT_LOCATION', None)
        if default_location:
            self.search_panel.set_location(default_location)
            self.search_panel.search()

    def configure_styles(self):
        """Configure custom styles for the application"""
        self.style.theme_use('clam')

        # Frame styles
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('Card.TFrame',
                             background='white',
                             borderwidth=1,
                             relief='groove',
                             padding=10)

        # Button styles
        self.style.configure('Accent.TButton',
                             foreground='white',
                             background='#4285f4',
                             font=('Arial', 10, 'bold'),
                             padding=5)
        self.style.map('Accent.TButton',
                       background=[('active', '#3367d6')])

        # Label styles
        self.style.configure('Title.TLabel',
                             font=('Arial', 12, 'bold'),
                             foreground='#333333')

        self.style.configure('Temp.TLabel',
                             font=('Arial', 48, 'bold'),
                             foreground='#222222')

    def create_widgets(self):
        """Create and arrange all widgets"""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Search panel
        self.search_panel = SearchPanel(
            main_frame,
            search_callback=self.handle_search,
            get_history_callback=self.get_search_history,
            unit_callback=self.handle_unit_change,
            padding=10
        )
        self.search_panel.pack(fill=tk.X, pady=(0, 10))

        # Current weather display
        self.current_weather = CurrentWeather(main_frame)
        self.current_weather.pack(fill=tk.BOTH, expand=True)

        # Forecast display
        forecast_label = ttk.Label(
            main_frame,
            text="5-Day Forecast",
            style='Title.TLabel'
        )
        forecast_label.pack(pady=(10, 5))

        self.forecast = ForecastDisplay(main_frame)
        self.forecast.pack(fill=tk.BOTH, expand=True)

    def handle_search(self, location: str):
        """Handle search requests"""
        if not location.strip():
            messagebox.showwarning("Warning", "Location cannot be empty.")
            return

        try:
            # Show loading state
            self.current_weather.set_loading_state()
            self.forecast.clear_data()

            # First, get lat/lon for location string
            location_results = APIHandler.get_location_results(location)

            if not location_results:
                messagebox.showerror("Error", f"Location '{location}' not found.")
                self.current_weather.set_empty_state()
                self.forecast.clear_data()
                return

            # Use first location result
            lat = location_results[0]['lat']
            lon = location_results[0]['lon']

            units = self.get_current_units()

            # Get current weather and forecast by lat, lon
            current_data = APIHandler.get_current_weather(lat, lon, units)
            forecast_data = APIHandler.get_forecast(lat, lon, units)

            if current_data and forecast_data:
    # Update displays
                 self.current_weather.update_data(current_data, units)
                 self.forecast.update_forecast(forecast_data, units)  # <-- FIXED METHOD NAME

    # Add to search history
                 if location not in self.search_history:
                   self.search_history.append(location)

            else:
                messagebox.showerror("Error", "Failed to fetch weather data.")
                self.current_weather.set_empty_state()
                self.forecast.clear_data()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.current_weather.set_empty_state()
            self.forecast.clear_data()

    def handle_unit_change(self, unit: str):
        """Handle unit changes (C/F)"""
        current_location = self.search_panel.get_current_location()
        if current_location:
            self.handle_search(current_location)

    def get_search_history(self) -> List[str]:
        """Return search history (last 10 items, most recent first)"""
        return self.search_history[-10:][::-1]

    def get_current_units(self) -> str:
        """Get current unit system (metric/imperial)"""
        unit = getattr(self.search_panel, 'unit_var', None)
        if unit:
            return 'metric' if unit.get() == 'C' else 'imperial'
        return 'metric'


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
