# utils.py
"""
Contains utility functions for the game, such as currency formatting.
"""
import tkinter as tk
from PIL import Image, ImageTk


def apply_tiled_background(widget, image_path):
    """
    Applies a tiled background image to a given widget.

    The image is drawn on a Canvas that is placed behind all other children
    of the widget. The canvas resizes with the widget to redraw the background.
    """
    try:
        # Open the image using PIL and store it on the widget to prevent
        # it from being garbage collected.
        pil_image = Image.open(image_path)
        setattr(widget, f'_bg_pil_{image_path.replace("/", "_")}', pil_image)

    except FileNotFoundError:
        # Fallback to a solid color if the image is not found.
        # A semi-dark grey that fits the theme
        widget.config(bg="#4a4a4a")
        print(f"Hintergrundbild nicht gefunden: {image_path}")
        return

    # Create a Canvas that will hold the background image
    canvas = tk.Canvas(widget)
    # Place it to fill the entire widget and send it to the back
    canvas.place(x=0, y=0, relwidth=1, relheight=1)
    canvas.lower()

    def tile_background(event):
        """Callback function to redraw the background when the widget is resized."""
        # Get the stored PIL image from the widget
        bg_pil_image = getattr(widget, f'_bg_pil_{image_path.replace("/", "_")}', None)
        if not bg_pil_image:
            return

        width = widget.winfo_width()
        height = widget.winfo_height()

        # If the window is not yet drawn, its size can be 1, so we do nothing
        if width <= 1 or height <= 1:
            return

        # Create a new blank image of the widget's size
        bg_image = Image.new('RGB', (width, height))
        tile_w, tile_h = bg_pil_image.size

        # Paste the tile across the new image
        for x in range(0, width, tile_w):
            for y in range(0, height, tile_h):
                bg_image.paste(bg_pil_image, (x, y))

        # Convert the PIL image to a PhotoImage that Tkinter can use.
        # Store a reference on the canvas to prevent garbage collection.
        canvas.bg_photo_tk = ImageTk.PhotoImage(bg_image)
        canvas.create_image(0, 0, image=canvas.bg_photo_tk, anchor='nw')

    # Bind the tiling function to the widget's <Configure> event
    widget.bind("<Configure>", tile_background, add="+")


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
