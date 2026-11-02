"""
Improved splash screen for Limbo Card Game GUI with better colors
"""

import tkinter as tk
from tkinter import ttk
import threading
import time

class SplashScreen:
    """Splash screen displayed during application startup with improved colors"""
    
    def __init__(self, parent):
        """Initialize splash screen"""
        self.parent = parent
        self.splash = tk.Toplevel()
        self.setup_splash()
        self.animate_loading()
    
    def setup_splash(self):
        """Setup splash screen appearance with better colors"""
        # Configure splash window
        self.splash.title("Limbo Card Game")
        self.splash.geometry("600x400")
        self.splash.resizable(False, False)
        
        # Center the splash screen
        self.center_window()
        
        # Remove window decorations
        self.splash.overrideredirect(True)
        
        # Create main frame with appealing gradient-like background
        main_frame = tk.Frame(self.splash, bg='#2e5c3e', relief='raised', bd=3)
        main_frame.pack(fill='both', expand=True)
        
        # Add decorative border
        border_frame = tk.Frame(main_frame, bg='#4a7c59', relief='sunken', bd=2)
        border_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        content_frame = tk.Frame(border_frame, bg='#5a8a69')
        content_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Title with shadow effect
        title_container = tk.Frame(content_frame, bg='#5a8a69')
        title_container.pack(pady=(60, 10))
        
        # Shadow
        title_shadow = tk.Label(
            title_container,
            text="LIMBO",
            font=('Arial Black', 56, 'bold'),
            fg='#1a3d2e',
            bg='#5a8a69'
        )
        title_shadow.place(x=2, y=2)
        
        # Main title
        title_main = tk.Label(
            title_container,
            text="LIMBO",
            font=('Arial Black', 56, 'bold'),
            fg='#87ceeb',
            bg='#5a8a69'
        )
        title_main.place(x=0, y=0)
        
        # Subtitle
        subtitle_label = tk.Label(
            content_frame,
            text="Strategic Card Game",
            font=('Arial', 20, 'bold'),
            fg='#ffffff',
            bg='#5a8a69'
        )
        subtitle_label.pack(pady=(80, 20))
        
        # Game description
        desc_label = tk.Label(
            content_frame,
            text="Reduce from 101 to zero • Division is mandatory • Last player wins",
            font=('Arial', 12),
            fg='#e0f0e0',
            bg='#5a8a69',
            justify='center'
        )
        desc_label.pack(pady=(0, 30))
        
        # Loading indicator
        self.loading_label = tk.Label(
            content_frame,
            text="Loading...",
            font=('Arial', 14, 'bold'),
            fg='#ffeb3b',
            bg='#5a8a69'
        )
        self.loading_label.pack(pady=(0, 15))
        
        # Progress bar with custom styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Horizontal.TProgressbar",
                       troughcolor='#2e5c3e',
                       background='#87ceeb',
                       borderwidth=1,
                       relief='sunken')
        
        self.progress = ttk.Progressbar(
            content_frame,
            length=350,
            mode='indeterminate',
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=(0, 40))
        
        # Version info
        version_label = tk.Label(
            content_frame,
            text="GUI Version 1.0 | Enhanced Edition",
            font=('Arial', 10),
            fg='#b0d0b0',
            bg='#5a8a69'
        )
        version_label.pack(side='bottom', pady=(0, 20))
        
        # Add decorative elements
        self.add_decorative_elements(content_frame)
    
    def add_decorative_elements(self, parent):
        """Add decorative card suit elements"""
        suits = ['♠', '♥', '♦', '♣']
        colors = ['#ffffff', '#ff6b6b', '#ff6b6b', '#ffffff']
        
        # Top decorative elements
        top_frame = tk.Frame(parent, bg='#5a8a69', height=30)
        top_frame.pack(side='top', fill='x')
        top_frame.pack_propagate(False)
        
        for i, (suit, color) in enumerate(zip(suits, colors)):
            x_pos = 100 + i * 100
            suit_label = tk.Label(
                top_frame,
                text=suit,
                font=('Arial', 20),
                fg=color,
                bg='#5a8a69'
            )
            suit_label.place(x=x_pos, y=5)
        
        # Bottom decorative elements
        bottom_frame = tk.Frame(parent, bg='#5a8a69', height=30)
        bottom_frame.pack(side='bottom', fill='x')
        bottom_frame.pack_propagate(False)
        
        for i, (suit, color) in enumerate(zip(suits[::-1], colors[::-1])):
            x_pos = 100 + i * 100
            suit_label = tk.Label(
                bottom_frame,
                text=suit,
                font=('Arial', 20),
                fg=color,
                bg='#5a8a69'
            )
            suit_label.place(x=x_pos, y=5)
    
    def center_window(self):
        """Center the splash screen on the screen"""
        self.splash.update_idletasks()
        width = self.splash.winfo_width()
        height = self.splash.winfo_height()
        x = (self.splash.winfo_screenwidth() // 2) - (width // 2)
        y = (self.splash.winfo_screenheight() // 2) - (height // 2)
        self.splash.geometry(f"{width}x{height}+{x}+{y}")
    
    def animate_loading(self):
        """Animate the loading progress bar"""
        self.progress.start(15)
        
        # Animate loading text
        threading.Thread(target=self.animate_text, daemon=True).start()
    
    def animate_text(self):
        """Animate loading text with dots"""
        loading_states = [
            "Loading",
            "Loading.",
            "Loading..",
            "Loading...",
            "Starting Game",
            "Starting Game.",
            "Starting Game..",
            "Starting Game...",
            "Ready to Play!"
        ]
        
        for i, state in enumerate(loading_states):
            try:
                self.loading_label.config(text=state)
                time.sleep(0.3)
            except tk.TclError:
                # Window was destroyed
                break
    
    def destroy(self):
        """Destroy the splash screen"""
        try:
            self.progress.stop()
            self.splash.destroy()
        except tk.TclError:
            pass