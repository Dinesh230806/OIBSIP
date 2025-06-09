# import sys
# from pathlib import Path

# # Add project root to Python path
# sys.path.insert(0, str(Path(__file__).parent))

# try:
#     from gui.app import WeatherApp
#     print("All imports successful!")
# except ImportError as e:
#     print(f"Import error: {e}")
#     print(f"Python path: {sys.path}")
#     print(f"Files in directory: {[f.name for f in Path(__file__).parent.iterdir()]}")
#     raise

# if __name__ == "__main__":
#     app = WeatherApp()
#     app.mainloop()



import sys
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

try:
    from gui.app import WeatherApp
    print("All imports successful!")
except ImportError as e:
    print(f"[Import Error] {e}")
    print(f"Python path: {sys.path}")
    print("Directory listing:")
    for file in BASE_DIR.iterdir():
        print(f"- {file.name}")
    raise

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()

