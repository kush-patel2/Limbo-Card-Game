"""
Main application window for Limbo Card Game GUI
Updated to support complete rule implementation
"""

import tkinter as tk
from tkinter import messagebox, ttk
from .menu_screen import MenuScreen
from .game_screen import GameScreen
from .rules_screen import RulesScreen
from .settings_screen import SettingsScreen
from core.game_manager import GameManager

class MainWindow:
    """Main application window managing different screens"""
    
    def __init__(self, root):
        """Initialize main window"""
        self.root = root
        self.game_manager = GameManager()
        self.current_screen = None
        
        self.setup_window()
        self.create_menu_bar()
        self.show_menu_screen()
    
    def setup_window(self):
        """Setup main window properties"""
        self.root.title("Limbo Card Game - Complete Rules Edition")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Center window on screen
        self.center_window()
        
        # Configure window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configure styling
        self.configure_styles()
        
        # Create main container
        self.main_container = tk.Frame(self.root, bg='#f0f0f0')
        self.main_container.pack(fill='both', expand=True)
    
    def center_window(self):
        """Center the main window on screen"""
        self.root.update_idletasks()
        width = 1200
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def configure_styles(self):
        """Configure ttk styles for consistent appearance"""
        style = ttk.Style()
        
        # Configure button styles
        style.configure(
            'Large.TButton',
            font=('Arial', 14, 'bold'),
            padding=(20, 10)
        )
        
        style.configure(
            'Medium.TButton',
            font=('Arial', 12),
            padding=(15, 8)
        )
        
        style.configure(
            'Small.TButton',
            font=('Arial', 10),
            padding=(10, 5)
        )
        
        # Configure label styles
        style.configure(
            'Title.TLabel',
            font=('Arial', 24, 'bold'),
            foreground='#1a1a2e'
        )
        
        style.configure(
            'Subtitle.TLabel',
            font=('Arial', 16, 'bold'),
            foreground='#16213e'
        )
        
        style.configure(
            'Info.TLabel',
            font=('Arial', 12),
            foreground='#0f3460'
        )
    
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Game", command=self.new_game)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Game menu
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="Main Menu", command=self.show_menu_screen)
        game_menu.add_command(label="Rules", command=self.show_rules_screen)
        game_menu.add_command(label="Settings", command=self.show_settings_screen)
        game_menu.add_separator()
        game_menu.add_command(label="Quick Human vs Human", command=self.quick_human_game)
        game_menu.add_command(label="Quick Human vs Computer", command=self.quick_ai_game)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="How to Play", command=self.show_rules_screen)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="What's New", command=self.show_whats_new)
    
    def clear_screen(self):
        """Clear current screen"""
        if self.current_screen:
            self.current_screen.destroy()
        
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def show_menu_screen(self):
        """Display main menu screen"""
        self.clear_screen()
        self.current_screen = MenuScreen(self.main_container, self)
    
    def show_game_screen(self, game_mode='human_vs_human'):
        """Display game screen"""
        self.clear_screen()
        self.current_screen = GameScreen(self.main_container, self, game_mode)
    
    def show_rules_screen(self):
        """Display rules screen"""
        self.clear_screen()
        self.current_screen = RulesScreen(self.main_container, self)
    
    def show_settings_screen(self):
        """Display settings screen"""
        self.clear_screen()
        self.current_screen = SettingsScreen(self.main_container, self)
    
    def new_game(self):
        """Start a new game"""
        if self.current_screen and hasattr(self.current_screen, 'confirm_new_game'):
            if self.current_screen.confirm_new_game():
                self.show_game_screen()
        else:
            self.show_game_screen()
    
    def quick_human_game(self):
        """Quick start human vs human game"""
        # Setup default human vs human game
        self.game_manager.setup_game(
            player1_name="Player 1",
            player2_name="Player 2",
            target_score=200,
            game_mode='human_vs_human'
        )
        self.show_game_screen('human_vs_human')
    
    def quick_ai_game(self):
        """Quick start human vs computer game"""
        # Setup default human vs computer game
        self.game_manager.setup_game(
            player1_name="Player",
            player2_name="Computer (Medium)",
            target_score=200,
            game_mode='human_vs_computer',
            ai_difficulty='Medium'
        )
        self.show_game_screen('human_vs_computer')
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Limbo Card Game - Complete Rules Edition

A strategic card game for two players where you must reduce
a count from 101 to zero without going below.

✨ NEW FEATURES:
• Complete card drawing mechanics
• Proper doubling phase implementation
• Forced card play from stock
• Enhanced AI with strategic thinking
• Improved visual feedback

Version: 2.0 (Complete Rules)
Platform: Python/Tkinter
Compatible: Windows, macOS, Linux

Based on David Parlett's original Limbo rules
Developed for Agile Development Project
© 2025 - Educational Use"""
        
        messagebox.showinfo("About Limbo Card Game", about_text)
    
    def show_whats_new(self):
        """Show what's new in this version"""
        whats_new_text = """What's New in Limbo v2.0

🎯 COMPLETE RULE IMPLEMENTATION:
• Card drawing when no playable cards
• Mandatory play of drawable cards
• Proper turn handling with stock pile
• Fixed starting card logic for face cards

🎲 ENHANCED DOUBLING SYSTEM:
• Full doubling/redoubling mechanics
• Visual indicators for stake multipliers
• AI strategic doubling decisions

🤖 IMPROVED AI:
• Better strategic thinking
• Proper handling of drawing scenarios
• Enhanced difficulty scaling

🎨 BETTER USER EXPERIENCE:
• Clear status indicators
• Drawing notifications
• Forced play indicators
• Enhanced visual feedback

🔧 BUG FIXES:
• Fixed score multiplier application
• Corrected turn switching logic
• Improved error handling
• Better state management

Now 100% compliant with official Limbo rules!"""
        
        messagebox.showinfo("What's New - Version 2.0", whats_new_text)
    
    def on_closing(self):
        """Handle application closing"""
        if self.current_screen and hasattr(self.current_screen, 'on_closing'):
            if not self.current_screen.on_closing():
                return
        
        if messagebox.askokcancel("Quit", "Do you want to quit the game?"):
            self.root.destroy()
    
    def get_game_manager(self):
        """Get the game manager instance"""
        return self.game_manager