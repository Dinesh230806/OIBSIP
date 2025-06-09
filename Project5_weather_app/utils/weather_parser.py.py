class WeatherParser:
    """Parses raw weather API data into structured formats"""
    
    @staticmethod
    def parse_current(data: dict) -> dict:
        """Parse current weather data from API response"""
        weather = data['weather'][0]
        main = data['main']
        wind = data.get('wind', {})
        
        return {
            'temp': main['temp'],
            'feels_like': main['feels_like'],
            'humidity': main['humidity'],
            'pressure': main['pressure'],
            'wind_speed': wind.get('speed', 0),
            'description': weather['description'],
            'icon': weather['icon'],
            'visibility': data.get('visibility', 'N/A'),
            'sunrise': data.get('sys', {}).get('sunrise'),
            'sunset': data.get('sys', {}).get('sunset')
        }

    @staticmethod
    def parse_forecast(data: dict) -> list:
        """Parse 5-day forecast data from API response"""
        forecast = []
        for item in data['list']:
            forecast.append({
                'datetime': item['dt_txt'],
                'temp': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'humidity': item['main']['humidity'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon'],
                'wind_speed': item.get('wind', {}).get('speed', 0)
            })
        return forecast