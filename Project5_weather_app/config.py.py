class Config:
    API_KEY = "c2daf6be5e1f5570af85faf5441f9ade"
    BASE_URL = "https://api.openweathermap.org/data/2.5/"
    GEO_URL = "http://api.openweathermap.org/geo/1.0/direct?q={}&limit=1&appid={}"
    ICON_URL = "https://openweathermap.org/img/wn/{}@2x.png"
    DEFAULT_LOCATION = "London,UK"
    UNITS = "metric"  # 'imperial' for Fahrenheit
    TIMEOUT = 10
