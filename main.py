#!/usr/bin/env python3
"""
Limbo Card Game - GUI Version
Main application entry point
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.main_window import MainWindow
from gui.splash_screen import SplashScreen

def main():
    """Main application entry point"""
    try:
        # Create root window
        root = tk.Tk()
        root.withdraw()  # Hide root initially
        
        # Show splash screen
        splash = SplashScreen(root)
        root.after(3000, lambda: start_main_app(root, splash))
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")
        sys.exit(1)

def start_main_app(root, splash):
    """Start the main application after splash screen"""
    try:
        splash.destroy()
        root.deiconify()  # Show root window
        
        # Create and start main application
        app = MainWindow(root)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start main application: {str(e)}")
        root.destroy()

if __name__ == "__main__":
    main()