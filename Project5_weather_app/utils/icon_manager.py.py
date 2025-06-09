from PIL import Image, ImageTk
import io
from tkinter import PhotoImage
from utils.api_handler import APIHandler

class IconManager:
    @staticmethod
    def get_icon_image(icon_code: str, size: tuple = (64, 64)) -> PhotoImage:
        """Get weather icon as Tkinter PhotoImage"""
        icon_data = APIHandler.get_weather_icon(icon_code)
        if icon_data:
            image = Image.open(io.BytesIO(icon_data))
            image = image.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        return None

    @staticmethod
    def get_default_icon(size: tuple = (64, 64)) -> PhotoImage:
        """Return a default icon when weather icon is not available"""
        from tkinter import PhotoImage
        # Create a simple placeholder
        img = Image.new('RGBA', size, (240, 240, 240, 0))
        return ImageTk.PhotoImage(img)