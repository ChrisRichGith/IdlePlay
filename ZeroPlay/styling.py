# styling.py
"""
Centralized styling setup for the ZeroPlay RPG application.
"""
from tkinter import ttk

def setup_styles():
    """
    Configures and returns a ttk.Style object with all custom styles for the app.
    This should be called once at application startup.
    """
    style = ttk.Style()

    # Set a base background color that complements the stone, for areas the leather doesn't cover.
    style.configure('TFrame', background='#4a4a4a')

    # Style for widgets on the leather background
    leather_bg_color = '#6F4E37' # Coffee brown, as a fallback and for matching
    leather_fg_color = '#F5DEB3' # Wheat color for text

    style.configure('Leather.TLabel', background=leather_bg_color, foreground=leather_fg_color, font=('Verdana', 9))
    style.configure('Leather.TLabelFrame', background=leather_bg_color)
    style.configure('Leather.TLabelFrame.Label', background=leather_bg_color, foreground=leather_fg_color, font=('Verdana', 10, 'bold'))

    # Style for Buttons on the leather background
    style.configure('Leather.TButton', background='#5D4037', foreground=leather_fg_color, font=('Verdana', 9, 'bold'), borderwidth=1)
    style.map('Leather.TButton',
        background=[('active', '#795548'), ('disabled', '#4E342E')],
        foreground=[('disabled', '#A1887F')])

    # Style for the Notebook (Tabs)
    style.configure('Leather.TNotebook', background=leather_bg_color, borderwidth=0)
    style.configure('Leather.TNotebook.Tab',
        background='#5D4037', # Darker brown for inactive tab
        foreground=leather_fg_color,
        padding=[8, 4],
        font=('Verdana', 9, 'bold')
    )
    style.map('Leather.TNotebook.Tab',
        background=[('selected', leather_bg_color)], # Active tab matches panel bg
        expand=[('selected', [1, 1, 1, 0])])

    return style
