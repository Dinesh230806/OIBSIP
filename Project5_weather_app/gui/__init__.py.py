"""
GUI package for the Weather Application
"""

# Import main classes to make them available at package level
from .app import WeatherApp
from .components.search_panel import SearchPanel
from .components.current_weather import CurrentWeather

# Version information
__version__ = "1.0.0"

# List of what's available when importing from gui
__all__ = [
    'WeatherApp',
    'SearchPanel',
    'CurrentWeather'
]