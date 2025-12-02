# utils.py
"""
Contains utility functions for the game, such as currency formatting.
"""
import tkinter as tk
from PIL import Image, ImageTk

def apply_tiled_background(widget, image_path):
    """
    Applies a tiled background image to a widget.

    The image is drawn on a canvas that resizes with the widget.
    A reference to the PhotoImage is stored on the canvas to prevent
    garbage collection.
    """
    try:
        # Open the original image
        original_image = Image.open(image_path)
    except FileNotFoundError:
        # If the image is not found, set a fallback background color
        widget.config(bg="#4a4a4a") # A neutral dark grey
        print(f"Warning: Background image not found at {image_path}")
        return

    # Create a canvas that will hold the background
    canvas = tk.Canvas(widget, highlightthickness=0)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    # Move the canvas to the bottom of the stacking order
    canvas.lower()

    # Store the original image as an attribute of the canvas so it's not garbage collected
    canvas.original_image = original_image

    def tile_background(event):
        """Callback to redraw the tiled background when the widget resizes."""
        # Get the current size of the canvas
        canvas_width = event.width
        canvas_height = event.height

        # Create a new blank image with the size of the canvas
        bg_image = Image.new('RGB', (canvas_width, canvas_height))

        # Tile the original image across the new background
        img_w, img_h = canvas.original_image.size
        for y in range(0, canvas_height, img_h):
            for x in range(0, canvas_width, img_w):
                bg_image.paste(canvas.original_image, (x, y))

        # Convert the PIL image to a PhotoImage
        # Store a reference on the canvas to prevent it from being garbage collected
        canvas.photo_image = ImageTk.PhotoImage(bg_image)

        # Set the canvas's background
        canvas.create_image(0, 0, image=canvas.photo_image, anchor='nw')

    # Bind the tiling function to the canvas's resize event
    canvas.bind('<Configure>', tile_background)


def format_currency(copper_amount):
    """
    Converts a total copper amount into a formatted string (gold, silver, copper).
    100 copper = 1 silver
    100 silver = 1 gold
    """
    if copper_amount == 0:
        return "0c"

    gold = copper_amount // 10000
    silver = (copper_amount % 10000) // 100
    copper = copper_amount % 100

    parts = []
    if gold > 0:
        parts.append(f"{gold}🪙")
    if silver > 0:
        parts.append(f"{silver}💿")
    if copper > 0:
        parts.append(f"{copper}🟤")

    return " ".join(parts)

def center_window(window, parent):
    """
    Centers a tkinter window over its parent window, handling multi-monitor setups.

    Args:
        window: The tkinter window (Toplevel) to center.
        parent: The parent window.
    """
    window.update_idletasks()

    # Get dimensions of the popup window
    width = window.winfo_width()
    height = window.winfo_height()

    # Get the position and dimensions of the parent window
    parent_x = parent.winfo_x()
    parent_y = parent.winfo_y()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()

    # Calculate the center position relative to the parent
    x = parent_x + (parent_width // 2) - (width // 2)
    y = parent_y + (parent_height // 2) - (height // 2)

    # Set the geometry of the popup window to place it correctly
    window.geometry(f'{width}x{height}+{x}+{y}')
