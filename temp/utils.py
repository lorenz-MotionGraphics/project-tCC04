# utils.py
import os
from PIL import Image, ImageTk

def set_icon(window, icon_filename="app_icon.ico"):
    try:
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), icon_filename)
        icon = ImageTk.PhotoImage(file=icon_path)
        window.wm_iconphoto(True, icon)
        window.icon_ref = icon  # Prevent garbage collection
    except Exception as e:
        print(f"Error setting icon: {e}")
