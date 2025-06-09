import requests
from config import Config
from typing import Dict, Optional, List, Tuple
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIHandler:
    @staticmethod
    def get_coordinates(location: str) -> Tuple[Optional[float], Optional[float]]:
        """
        Get latitude and longitude for a location (simplified version of get_location_results)
        Args:
            location: City name (e.g., "London,UK")
        Returns:
            Tuple of (lat, lon) or (None, None) if not found
        """
        try:
            results = APIHandler.get_location_results(location, limit=1)
            return (results[0]['lat'], results[0]['lon']) if results else (None, None)
        except Exception as e:
            logger.error(f"Error getting coordinates: {e}")
            return None, None

    @staticmethod
    def get_location_results(query: str, limit: int = 5) -> List[Dict]:
        """
        Get precise location matches using direct geocoding with enhanced query handling
        Args:
            query: Location search string (e.g., "London,UK")
            limit: Maximum number of results to return
        Returns:
            List of location dictionaries or empty list on error
        """
        try:
            # Normalize the query
            query = query.strip()
            if ',' not in query:
                query = f"{query},"

            url = "http://api.openweathermap.org/geo/1.0/direct"
            params = {
                'q': query,
                'limit': limit,
                'appid': Config.API_KEY
            }
            
            logger.info(f"Fetching location results for: {query}")
            response = requests.get(url, params=params, timeout=Config.TIMEOUT)
            response.raise_for_status()
            
            results = response.json()
            
            # If no results, try with just the city name
            if not results and ',' in query:
                city_only = query.split(',')[0]
                logger.info(f"Trying fallback search for: {city_only}")
                params['q'] = city_only
                response = requests.get(url, params=params, timeout=Config.TIMEOUT)
                response.raise_for_status()
                results = response.json()
            
            return results

        except requests.exceptions.RequestException as e:
            logger.error(f"Geocoding API Error for query '{query}': {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in get_location_results: {e}")
            return []

    @staticmethod
    def get_current_weather(lat: float, lon: float, units: str = Config.UNITS) -> Optional[Dict]:
        """
        Fetch current weather by coordinates with enhanced error handling
        Args:
            lat: Latitude
            lon: Longitude
            units: Measurement units ('metric' or 'imperial')
        Returns:
            Weather data dictionary or None on error
        """
        try:
            url = f"{Config.BASE_URL}weather"
            params = {
                'lat': lat,
                'lon': lon,
                'units': units,
                'appid': Config.API_KEY,
                'lang': 'en'
            }
            
            logger.info(f"Fetching current weather for coordinates: {lat},{lon}")
            response = requests.get(url, params=params, timeout=Config.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            
            # Validate response structure
            required_keys = {'main', 'weather', 'name', 'sys', 'wind'}
            if not all(key in data for key in required_keys):
                missing = required_keys - set(data.keys())
                raise ValueError(f"Missing keys in response: {missing}")
                
            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"Current weather API Error: {e}")
            return None
        except ValueError as e:
            logger.error(f"Data validation error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in get_current_weather: {e}")
            return None

    @staticmethod
    def get_forecast(lat: float, lon: float, units: str = Config.UNITS) -> Optional[Dict]:
        """
        Fetch 5-day forecast by coordinates with improved data validation
        Args:
            lat: Latitude
            lon: Longitude
            units: Measurement units ('metric' or 'imperial')
        Returns:
            Forecast data dictionary or None on error
        """
        try:
            url = f"{Config.BASE_URL}forecast"
            params = {
                'lat': lat,
                'lon': lon,
                'units': units,
                'appid': Config.API_KEY,
                'cnt': 40,
                'lang': 'en'
            }
            
            logger.info(f"Fetching forecast for coordinates: {lat},{lon}")
            response = requests.get(url, params=params, timeout=Config.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            
            # Validate forecast data structure
            if 'list' not in data or not isinstance(data['list'], list):
                raise ValueError("Invalid forecast data structure")
            if len(data['list']) == 0:
                raise ValueError("Empty forecast data")
                
            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"Forecast API Error: {e}")
            return None
        except ValueError as e:
            logger.error(f"Forecast data validation error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in get_forecast: {e}")
            return None

    @staticmethod
    def get_weather_icon(icon_code: str, size: tuple = (64, 64)) -> Optional[bytes]:
        """
        Download weather icon with improved retry logic
        Args:
            icon_code: Weather icon code (e.g., '01d')
            size: Tuple of (width, height) for resizing
        Returns:
            Icon image bytes or None on error
        """
        try:
            url = Config.ICON_URL.format(icon_code)
            
            for attempt in range(3):
                try:
                    logger.info(f"Fetching weather icon: {icon_code} (attempt {attempt + 1})")
                    response = requests.get(url, timeout=5)
                    response.raise_for_status()
                    return response.content
                except requests.exceptions.Timeout:
                    if attempt == 2:
                        raise
                    continue
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"Weather icon download error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in get_weather_icon: {e}")
            return None

    @staticmethod
    def get_weather_by_city(city: str, country_code: str = None, 
                           units: str = Config.UNITS) -> Optional[Dict]:
        """
        High-level method to get weather for a city with location fallback
        Args:
            city: City name
            country_code: Optional country code (e.g., 'US')
            units: Measurement units ('metric' or 'imperial')
        Returns:
            Dictionary with 'current' and 'forecast' data or None on error
        """
        try:
            # Build location query
            query = f"{city},{country_code}" if country_code else city
            logger.info(f"Getting weather for location: {query}")
            
            # Get location coordinates
            locations = APIHandler.get_location_results(query)
            if not locations:
                logger.warning(f"No location results found for: {query}")
                return None
                
            # Use best match (prioritize exact matches)
            lat, lon = locations[0]['lat'], locations[0]['lon']
            
            # Get weather data
            current = APIHandler.get_current_weather(lat, lon, units)
            forecast = APIHandler.get_forecast(lat, lon, units)
            
            if not current or not forecast:
                logger.warning(f"Incomplete weather data for: {query}")
                return None
                
            return {
                'location': {
                    'name': locations[0]['name'],
                    'country': locations[0]['country'],
                    'lat': lat,
                    'lon': lon
                },
                'current': current,
                'forecast': forecast
            }

        except Exception as e:
            logger.error(f"Error in get_weather_by_city: {e}")
            return None

    @staticmethod
    def get_formatted_location_name(location_data: Dict) -> str:
        """
        Format location name consistently
        Args:
            location_data: Dictionary with location info
        Returns:
            Formatted string (e.g., "London, UK")
        """
        try:
            name = location_data.get('name', 'Unknown Location')
            country = location_data.get('country', '')
            
            # Handle common country code variations
            country = country.upper()
            if country == 'GB':
                country = 'UK'
                
            return f"{name}, {country}" if country else name
        except Exception as e:
            logger.error(f"Error formatting location name: {e}")
            return "Unknown Location"