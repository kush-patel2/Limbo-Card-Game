"""
Colorful main menu screen for Limbo Card Game GUI
Enhanced with better colors and appealing design
"""

import tkinter as tk
from tkinter import ttk
from .player_setup_dialog import PlayerSetupDialog

class MenuScreen:
    """Main menu screen with enhanced colors and design"""
    
    def __init__(self, parent, main_window):
        """Initialize menu screen"""
        self.parent = parent
        self.main_window = main_window
        self.frame = None
        self.create_screen()
    
    def create_screen(self):
        """Create the menu screen layout with better colors"""
        # Main frame with appealing forest green background
        self.frame = tk.Frame(self.parent, bg='#2e5c3e')
        self.frame.pack(fill='both', expand=True)
        
        # Create the main content
        self.create_background()
        self.create_header()
        self.create_game_modes()
        self.create_quick_info()
        self.create_footer()
    
    def create_background(self):
        """Create an attractive background with card patterns"""
        # Create canvas for background effects
        self.canvas = tk.Canvas(self.frame, highlightthickness=0, bg='#2e5c3e')
        self.canvas.pack(fill='both', expand=True)
        
        # Create subtle card pattern background
        self.create_card_pattern()
        
        # Main content container with rounded appearance
        self.content_frame = tk.Frame(
            self.canvas, 
            bg='#4a7c59', 
            relief='raised', 
            bd=3
        )
        self.canvas.create_window(600, 400, window=self.content_frame, width=900, height=650)
    
    def create_card_pattern(self):
        """Create decorative card pattern in background"""
        # Create subtle card symbols in background
        symbols = ['♠', '♥', '♦', '♣']
        colors = ['#3a6c4a', '#4a7c5a', '#5a8c6a', '#3a6c4a']
        
        # Create a subtle pattern
        for i in range(0, 1200, 120):
            for j in range(0, 800, 120):
                symbol = symbols[(i + j) // 120 % 4]
                color = colors[(i + j) // 120 % 4]
                self.canvas.create_text(
                    i + 60, j + 60,
                    text=symbol,
                    font=('Arial', 28),
                    fill=color,
                    anchor='center'
                )
    
    def create_header(self):
        """Create impressive header section"""
        # Header background
        header_frame = tk.Frame(self.content_frame, bg='#5a8a69', relief='raised', bd=2)
        header_frame.pack(fill='x', pady=(20, 15))
        
        header_content = tk.Frame(header_frame, bg='#5a8a69')
        header_content.pack(fill='x', padx=30, pady=25)
        
        # Main title with glow effect
        title_container = tk.Frame(header_content, bg='#5a8a69')
        title_container.pack()
        
        # Shadow effect
        title_shadow = tk.Label(
            title_container,
            text="LIMBO",
            font=('Arial Black', 48, 'bold'),
            fg='#1a3d2e',
            bg='#5a8a69'
        )
        title_shadow.place(x=3, y=3)
        
        # Main title
        title_main = tk.Label(
            title_container,
            text="LIMBO",
            font=('Arial Black', 48, 'bold'),
            fg='#87ceeb',
            bg='#5a8a69'
        )
        title_main.place(x=0, y=0)
        
        # Ensure proper sizing
        title_container.update_idletasks()
        title_container.config(width=300, height=80)
        
        # Subtitle
        subtitle = tk.Label(
            header_content,
            text="THE STRATEGIC CARD GAME",
            font=('Arial', 18, 'bold'),
            fg='#ffffff',
            bg='#5a8a69'
        )
        subtitle.pack(pady=(80, 10))
        
        # Game description
        desc = tk.Label(
            header_content,
            text="Reduce from 101 to zero • Division is mandatory • Last player wins",
            font=('Arial', 14),
            fg='#e0f0e0',
            bg='#5a8a69'
        )
        desc.pack(pady=(5, 0))
    
    def create_game_modes(self):
        """Create game mode selection with attractive buttons"""
        modes_frame = tk.Frame(self.content_frame, bg='#4a7c59')
        modes_frame.pack(fill='x', padx=40, pady=20)
        
        # Section title
        title = tk.Label(
            modes_frame,
            text="CHOOSE GAME MODE",
            font=('Arial', 16, 'bold'),
            fg='#87ceeb',
            bg='#4a7c59'
        )
        title.pack(pady=(0, 20))
        
        # Game mode buttons in a grid
        buttons_frame = tk.Frame(modes_frame, bg='#4a7c59')
        buttons_frame.pack()
        
        # Configure grid
        buttons_frame.grid_rowconfigure(0, weight=1)
        buttons_frame.grid_rowconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        
        # Human vs Human button
        self.create_mode_button(
            buttons_frame,
            "👥 HUMAN vs HUMAN",
            "Play against a friend on the same computer",
            self.start_human_vs_human,
            0, 0,
            '#4a90e2'  # Blue
        )
        
        # Human vs Computer button
        self.create_mode_button(
            buttons_frame,
            "🤖 HUMAN vs COMPUTER",
            "Challenge our intelligent AI opponent",
            self.start_human_vs_computer,
            0, 1,
            '#28a745'  # Green
        )
        
        # Rules button
        self.create_mode_button(
            buttons_frame,
            "📚 LEARN TO PLAY",
            "Complete rules and strategy guide",
            self.show_rules,
            1, 0,
            '#ff8c42'  # Orange
        )
        
        # Settings button
        self.create_mode_button(
            buttons_frame,
            "⚙️ SETTINGS",
            "Customize your game experience",
            self.show_settings,
            1, 1,
            '#6f42c1'  # Purple
        )
    
    def create_mode_button(self, parent, title, description, command, row, col, color):
        """Create a stylized game mode button"""
        button_frame = tk.Frame(parent, bg='#5a8a69', relief='raised', bd=2)
        button_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew', ipadx=10, ipady=10)
        
        # Main button
        btn = tk.Button(
            button_frame,
            text=title,
            font=('Arial', 14, 'bold'),
            fg='#ffffff',
            bg=color,
            activebackground=self.lighten_color(color),
            activeforeground='#ffffff',
            relief='raised',
            bd=3,
            padx=20,
            pady=15,
            command=command,
            cursor='hand2'
        )
        btn.pack(fill='x', padx=8, pady=8)
        
        # Description
        desc = tk.Label(
            button_frame,
            text=description,
            font=('Arial', 10),
            fg='#ffffff',
            bg='#5a8a69',
            wraplength=220,
            justify='center'
        )
        desc.pack(pady=(0, 8))
        
        # Hover effects
        def on_enter(e):
            btn.config(bg=self.lighten_color(color))
            button_frame.config(bg='#6a9a79')
            
        def on_leave(e):
            btn.config(bg=color)
            button_frame.config(bg='#5a8a69')
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
    
    def lighten_color(self, color):
        """Lighten a hex color for hover effects"""
        color_map = {
            '#4a90e2': '#5ba0f2',
            '#28a745': '#38b755',
            '#ff8c42': '#ff9c52',
            '#6f42c1': '#7f52d1'
        }
        return color_map.get(color, color)
    
    def create_quick_info(self):
        """Create quick game info section"""
        info_frame = tk.LabelFrame(
            self.content_frame,
            text="Quick Game Overview",
            font=('Arial', 12, 'bold'),
            fg='#87ceeb',
            bg='#4a7c59',
            padx=20,
            pady=10
        )
        info_frame.pack(fill='x', padx=40, pady=15)
        
        # Info columns
        info_container = tk.Frame(info_frame, bg='#4a7c59')
        info_container.pack(fill='x')
        
        # Left column
        left_col = tk.Frame(info_container, bg='#4a7c59')
        left_col.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
        self.create_info_item(left_col, "🎯 Objective", "Be the last to play a card")
        self.create_info_item(left_col, "🔢 Starting Count", "101 points")
        self.create_info_item(left_col, "⚡ Key Rule", "Division is mandatory when possible")
        
        # Right column
        right_col = tk.Frame(info_container, bg='#4a7c59')
        right_col.pack(side='right', fill='both', expand=True, padx=(20, 0))
        
        self.create_info_item(right_col, "🏆 Win Condition", "Reduce count to exactly zero")
        self.create_info_item(right_col, "🎴 Special Cards", "Kings, Queens, Jacks, Aces")
        self.create_info_item(right_col, "⏱️ Game Length", "5-15 minutes per round")
    
    def create_info_item(self, parent, title, description):
        """Create an info item"""
        item_frame = tk.Frame(parent, bg='#4a7c59')
        item_frame.pack(fill='x', pady=3)
        
        title_label = tk.Label(
            item_frame,
            text=title,
            font=('Arial', 11, 'bold'),
            fg='#87ceeb',
            bg='#4a7c59'
        )
        title_label.pack(anchor='w')
        
        desc_label = tk.Label(
            item_frame,
            text=description,
            font=('Arial', 10),
            fg='#ffffff',
            bg='#4a7c59'
        )
        desc_label.pack(anchor='w', padx=(20, 0))
    
    def create_footer(self):
        """Create footer with version and exit"""
        footer_frame = tk.Frame(self.content_frame, bg='#3a6c4a', relief='sunken', bd=2)
        footer_frame.pack(side='bottom', fill='x', pady=(15, 20))
        
        footer_content = tk.Frame(footer_frame, bg='#3a6c4a')
        footer_content.pack(pady=15)
        
        # Version info
        version = tk.Label(
            footer_content,
            text="Limbo Card Game v1.0 | Enhanced GUI Edition",
            font=('Arial', 11, 'bold'),
            fg='#ffffff',
            bg='#3a6c4a'
        )
        version.pack()
        
        # Platform info
        platform = tk.Label(
            footer_content,
            text="Python/Tkinter • Cross-Platform Compatible",
            font=('Arial', 9),
            fg='#e0f0e0',
            bg='#3a6c4a'
        )
        platform.pack(pady=(5, 10))
        
        # Exit button
        exit_btn = tk.Button(
            footer_content,
            text="EXIT GAME",
            font=('Arial', 10, 'bold'),
            fg='#ffffff',
            bg='#dc3545',
            activebackground='#c82333',
            activeforeground='#ffffff',
            relief='raised',
            bd=2,
            padx=20,
            pady=8,
            command=self.exit_game,
            cursor='hand2'
        )
        exit_btn.pack()
        
        # Hover effect for exit button
        def on_exit_enter(e):
            exit_btn.config(bg='#e74c3c')
        
        def on_exit_leave(e):
            exit_btn.config(bg='#dc3545')
        
        exit_btn.bind('<Enter>', on_exit_enter)
        exit_btn.bind('<Leave>', on_exit_leave)
    
    def start_human_vs_human(self):
        """Start human vs human game"""
        dialog = PlayerSetupDialog(self.frame, "Human vs Human Game")
        
        if dialog.result:
            player1_name, player2_name, target_score = dialog.result
            
            # Configure game manager
            game_manager = self.main_window.get_game_manager()
            game_manager.setup_game(
                player1_name=player1_name,
                player2_name=player2_name,
                target_score=target_score,
                game_mode='human_vs_human'
            )
            
            # Start game
            self.main_window.show_game_screen('human_vs_human')
    
    def start_human_vs_computer(self):
        """Start human vs computer game"""
        dialog = PlayerSetupDialog(self.frame, "Human vs Computer Game", show_ai_options=True)
        
        if dialog.result:
            player_name, ai_difficulty, target_score = dialog.result
            
            # Configure game manager
            game_manager = self.main_window.get_game_manager()
            game_manager.setup_game(
                player1_name=player_name,
                player2_name=f"Computer ({ai_difficulty})",
                target_score=target_score,
                game_mode='human_vs_computer',
                ai_difficulty=ai_difficulty
            )
            
            # Start game
            self.main_window.show_game_screen('human_vs_computer')
    
    def show_rules(self):
        """Show game rules"""
        self.main_window.show_rules_screen()
    
    def show_settings(self):
        """Show settings screen"""
        self.main_window.show_settings_screen()
    
    def exit_game(self):
        """Exit the application"""
        self.main_window.on_closing()
    
    def destroy(self):
        """Destroy the menu screen"""
        if self.frame:
            self.frame.destroy()