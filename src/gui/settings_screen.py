"""
Settings screen for Limbo Card Game GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import json
import os

class SettingsScreen:
    """Screen for game settings and preferences"""
    
    def __init__(self, parent, main_window):
        """Initialize settings screen"""
        self.parent = parent
        self.main_window = main_window
        
        # Default settings
        self.default_settings = {
            'target_score': 200,
            'animation_speed': 'Medium',
            'sound_enabled': True,
            'auto_play_stock': True,
            'show_card_hints': True,
            'theme': 'Default',
            'ai_difficulty': 'Medium',
            'confirm_actions': True,
            'show_strategy_tips': True,
            'card_back_color': '#1a4d72'
        }
        
        # Load current settings
        self.settings = self.load_settings()
        
        self.create_screen()
    
    def create_screen(self):
        """Create the settings screen layout"""
        # Main frame
        self.frame = tk.Frame(self.parent, bg='#f0f0f0')
        self.frame.pack(fill='both', expand=True)
        
        # Create header
        self.create_header()
        
        # Create settings content
        self.create_settings_content()
        
        # Create footer
        self.create_footer()
    
    def create_header(self):
        """Create screen header"""
        header_frame = tk.Frame(self.frame, bg='#1a1a2e', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="GAME SETTINGS",
            font=('Arial', 24, 'bold'),
            fg='#ffffff',
            bg='#1a1a2e'
        )
        title_label.pack(expand=True)
    
    def create_settings_content(self):
        """Create settings content area"""
        content_frame = tk.Frame(self.frame, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Create notebook for categories
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Create setting tabs
        self.create_game_settings_tab()
        self.create_display_settings_tab()
        self.create_ai_settings_tab()
        self.create_advanced_settings_tab()
    
    def create_game_settings_tab(self):
        """Create game settings tab"""
        game_frame = tk.Frame(self.notebook, bg='white', padx=30, pady=30)
        self.notebook.add(game_frame, text="🎮 Game")
        
        # Default target score
        self.create_setting_section(
            game_frame,
            "Default Target Score",
            "The default score needed to win a game"
        )
        
        target_frame = tk.Frame(game_frame, bg='white')
        target_frame.pack(fill='x', pady=(5, 20))
        
        tk.Label(
            target_frame,
            text="Target Score:",
            font=('Arial', 12),
            bg='white'
        ).pack(side='left')
        
        self.target_score_var = tk.StringVar(value=str(self.settings['target_score']))
        target_spinbox = tk.Spinbox(
            target_frame,
            from_=50,
            to=1000,
            increment=50,
            textvariable=self.target_score_var,
            font=('Arial', 12),
            width=10
        )
        target_spinbox.pack(side='left', padx=(10, 0))
        
        # Auto-play stock card
        self.create_setting_section(
            game_frame,
            "Automatic Stock Play",
            "Automatically play stock card when player runs out of cards"
        )
        
        self.auto_play_var = tk.BooleanVar(value=self.settings['auto_play_stock'])
        tk.Checkbutton(
            game_frame,
            text="Auto-play stock card when possible",
            variable=self.auto_play_var,
            font=('Arial', 12),
            bg='white'
        ).pack(anchor='w', pady=(5, 20))
        
        # Confirm actions
        self.create_setting_section(
            game_frame,
            "Action Confirmation",
            "Show confirmation dialogs for important actions"
        )
        
        self.confirm_actions_var = tk.BooleanVar(value=self.settings['confirm_actions'])
        tk.Checkbutton(
            game_frame,
            text="Confirm card plays and game actions",
            variable=self.confirm_actions_var,
            font=('Arial', 12),
            bg='white'
        ).pack(anchor='w', pady=(5, 20))
        
        # Show strategy tips
        self.create_setting_section(
            game_frame,
            "Strategy Assistance",
            "Show helpful tips and strategy suggestions"
        )
        
        self.strategy_tips_var = tk.BooleanVar(value=self.settings['show_strategy_tips'])
        tk.Checkbutton(
            game_frame,
            text="Show strategy tips and hints",
            variable=self.strategy_tips_var,
            font=('Arial', 12),
            bg='white'
        ).pack(anchor='w', pady=(5, 20))
    
    def create_display_settings_tab(self):
        """Create display settings tab"""
        display_frame = tk.Frame(self.notebook, bg='white', padx=30, pady=30)
        self.notebook.add(display_frame, text="🎨 Display")
        
        # Animation speed
        self.create_setting_section(
            display_frame,
            "Animation Speed",
            "Speed of card animations and transitions"
        )
        
        anim_frame = tk.Frame(display_frame, bg='white')
        anim_frame.pack(fill='x', pady=(5, 20))
        
        tk.Label(
            anim_frame,
            text="Animation Speed:",
            font=('Arial', 12),
            bg='white'
        ).pack(side='left')
        
        self.animation_speed_var = tk.StringVar(value=self.settings['animation_speed'])
        animation_combo = ttk.Combobox(
            anim_frame,
            textvariable=self.animation_speed_var,
            values=['Slow', 'Medium', 'Fast', 'Off'],
            state='readonly',
            width=15
        )
        animation_combo.pack(side='left', padx=(10, 0))
        
        # Theme selection
        self.create_setting_section(
            display_frame,
            "Visual Theme",
            "Color scheme and visual appearance"
        )
        
        theme_frame = tk.Frame(display_frame, bg='white')
        theme_frame.pack(fill='x', pady=(5, 20))
        
        tk.Label(
            theme_frame,
            text="Theme:",
            font=('Arial', 12),
            bg='white'
        ).pack(side='left')
        
        self.theme_var = tk.StringVar(value=self.settings['theme'])
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=['Default', 'Dark', 'Light', 'Classic'],
            state='readonly',
            width=15
        )
        theme_combo.pack(side='left', padx=(10, 0))
        
        # Card back color
        self.create_setting_section(
            display_frame,
            "Card Back Color",
            "Color of the back of cards"
        )
        
        color_frame = tk.Frame(display_frame, bg='white')
        color_frame.pack(fill='x', pady=(5, 20))
        
        self.card_back_color = self.settings['card_back_color']
        
        self.color_preview = tk.Label(
            color_frame,
            text="   Preview   ",
            font=('Arial', 12),
            bg=self.card_back_color,
            fg='white',
            relief='raised',
            bd=2
        )
        self.color_preview.pack(side='left')
        
        ttk.Button(
            color_frame,
            text="Choose Color",
            command=self.choose_card_color
        ).pack(side='left', padx=(10, 0))
        
        # Show card hints
        self.create_setting_section(
            display_frame,
            "Card Hints",
            "Show helpful information about cards and moves"
        )
        
        self.card_hints_var = tk.BooleanVar(value=self.settings['show_card_hints'])
        tk.Checkbutton(
            display_frame,
            text="Show card effect hints on hover",
            variable=self.card_hints_var,
            font=('Arial', 12),
            bg='white'
        ).pack(anchor='w', pady=(5, 20))
    
    def create_ai_settings_tab(self):
        """Create AI settings tab"""
        ai_frame = tk.Frame(self.notebook, bg='white', padx=30, pady=30)
        self.notebook.add(ai_frame, text="🤖 AI")
        
        # Default AI difficulty
        self.create_setting_section(
            ai_frame,
            "Default AI Difficulty",
            "Default difficulty when playing against computer"
        )
        
        difficulty_frame = tk.Frame(ai_frame, bg='white')
        difficulty_frame.pack(fill='x', pady=(5, 20))
        
        tk.Label(
            difficulty_frame,
            text="AI Difficulty:",
            font=('Arial', 12),
            bg='white'
        ).pack(side='left')
        
        self.ai_difficulty_var = tk.StringVar(value=self.settings['ai_difficulty'])
        difficulty_combo = ttk.Combobox(
            difficulty_frame,
            textvariable=self.ai_difficulty_var,
            values=['Easy', 'Medium', 'Hard'],
            state='readonly',
            width=15
        )
        difficulty_combo.pack(side='left', padx=(10, 0))
        
        # AI behavior description
        self.create_setting_section(
            ai_frame,
            "AI Difficulty Levels",
            "What each difficulty level means"
        )
        
        descriptions = {
            'Easy': "Makes basic moves, occasional mistakes, thinks quickly",
            'Medium': "Good strategy, considers opponent moves, balanced play",
            'Hard': "Advanced strategy, multiple move lookahead, challenging"
        }
        
        for level, desc in descriptions.items():
            level_frame = tk.Frame(ai_frame, bg='#f8f8f8', relief='solid', bd=1)
            level_frame.pack(fill='x', pady=2)
            
            tk.Label(
                level_frame,
                text=f"{level}:",
                font=('Arial', 12, 'bold'),
                bg='#f8f8f8'
            ).pack(side='left', padx=10, pady=5)
            
            tk.Label(
                level_frame,
                text=desc,
                font=('Arial', 11),
                bg='#f8f8f8',
                wraplength=400
            ).pack(side='left', padx=(0, 10), pady=5)
    
    def create_advanced_settings_tab(self):
        """Create advanced settings tab"""
        advanced_frame = tk.Frame(self.notebook, bg='white', padx=30, pady=30)
        self.notebook.add(advanced_frame, text="⚙️ Advanced")
        
        # Sound settings (placeholder)
        self.create_setting_section(
            advanced_frame,
            "Sound Effects",
            "Enable or disable game sound effects"
        )
        
        self.sound_enabled_var = tk.BooleanVar(value=self.settings['sound_enabled'])
        tk.Checkbutton(
            advanced_frame,
            text="Enable sound effects (placeholder)",
            variable=self.sound_enabled_var,
            font=('Arial', 12),
            bg='white',
            state='disabled'  # Not implemented yet
        ).pack(anchor='w', pady=(5, 20))
        
        # Settings file location
        self.create_setting_section(
            advanced_frame,
            "Settings Storage",
            "Where your settings are saved"
        )
        
        settings_path = self.get_settings_path()
        tk.Label(
            advanced_frame,
            text=f"Settings file: {settings_path}",
            font=('Arial', 10),
            fg='#666',
            bg='white',
            wraplength=500
        ).pack(anchor='w', pady=(5, 10))
        
        # Reset settings
        self.create_setting_section(
            advanced_frame,
            "Reset Settings",
            "Restore all settings to default values"
        )
        
        ttk.Button(
            advanced_frame,
            text="Reset to Defaults",
            command=self.reset_to_defaults
        ).pack(anchor='w', pady=(5, 20))
        
        # Export/Import settings
        self.create_setting_section(
            advanced_frame,
            "Backup Settings",
            "Export or import your settings"
        )
        
        backup_frame = tk.Frame(advanced_frame, bg='white')
        backup_frame.pack(fill='x', pady=(5, 20))
        
        ttk.Button(
            backup_frame,
            text="Export Settings",
            command=self.export_settings
        ).pack(side='left', padx=(0, 10))
        
        ttk.Button(
            backup_frame,
            text="Import Settings",
            command=self.import_settings
        ).pack(side='left')
    
    def create_setting_section(self, parent, title, description):
        """Create a setting section with title and description"""
        section_frame = tk.Frame(parent, bg='white')
        section_frame.pack(fill='x', pady=(0, 5))
        
        tk.Label(
            section_frame,
            text=title,
            font=('Arial', 14, 'bold'),
            fg='#1a1a2e',
            bg='white'
        ).pack(anchor='w')
        
        tk.Label(
            section_frame,
            text=description,
            font=('Arial', 10),
            fg='#666',
            bg='white',
            wraplength=500
        ).pack(anchor='w')
    
    def choose_card_color(self):
        """Open color chooser for card back color"""
        color = colorchooser.askcolor(
            color=self.card_back_color,
            title="Choose Card Back Color"
        )
        
        if color[1]:  # If a color was chosen
            self.card_back_color = color[1]
            self.color_preview.config(bg=self.card_back_color)
    
    def create_footer(self):
        """Create footer with action buttons"""
        footer_frame = tk.Frame(self.frame, bg='#e0e0e0', height=80)
        footer_frame.pack(fill='x')
        footer_frame.pack_propagate(False)
        
        # Button frame
        button_frame = tk.Frame(footer_frame, bg='#e0e0e0')
        button_frame.pack(expand=True)
        
        # Save settings button
        ttk.Button(
            button_frame,
            text="💾 Save Settings",
            command=self.save_settings,
            style='Large.TButton'
        ).pack(side='left', padx=20, pady=20)
        
        # Cancel button
        ttk.Button(
            button_frame,
            text="❌ Cancel",
            command=self.cancel_changes,
            style='Large.TButton'
        ).pack(side='left', padx=20, pady=20)
        
        # Main menu button
        ttk.Button(
            button_frame,
            text="🏠 Main Menu",
            command=self.return_to_menu,
            style='Large.TButton'
        ).pack(side='left', padx=20, pady=20)
    
    def get_settings_path(self):
        """Get the path to the settings file"""
        return os.path.join(os.path.expanduser("~"), ".limbo_settings.json")
    
    def load_settings(self):
        """Load settings from file"""
        settings_path = self.get_settings_path()
        
        try:
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    loaded_settings = json.load(f)
                
                # Merge with defaults (in case new settings were added)
                settings = self.default_settings.copy()
                settings.update(loaded_settings)
                return settings
        except Exception as e:
            print(f"Error loading settings: {e}")
        
        return self.default_settings.copy()
    
    def save_current_settings(self):
        """Save current settings from UI"""
        try:
            self.settings.update({
                'target_score': int(self.target_score_var.get()),
                'animation_speed': self.animation_speed_var.get(),
                'sound_enabled': self.sound_enabled_var.get(),
                'auto_play_stock': self.auto_play_var.get(),
                'show_card_hints': self.card_hints_var.get(),
                'theme': self.theme_var.get(),
                'ai_difficulty': self.ai_difficulty_var.get(),
                'confirm_actions': self.confirm_actions_var.get(),
                'show_strategy_tips': self.strategy_tips_var.get(),
                'card_back_color': self.card_back_color
            })
            return True
        except ValueError as e:
            messagebox.showerror("Invalid Setting", f"Please check your input: {e}")
            return False
    
    def save_settings(self):
        """Save settings to file"""
        if not self.save_current_settings():
            return
        
        settings_path = self.get_settings_path()
        
        try:
            with open(settings_path, 'w') as f:
                json.dump(self.settings, f, indent=2)
            
            messagebox.showinfo("Settings Saved", "Your settings have been saved successfully!")
            self.return_to_menu()
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save settings: {e}")
    
    def cancel_changes(self):
        """Cancel changes and return to menu"""
        if messagebox.askyesno("Cancel Changes", "Are you sure you want to discard your changes?"):
            self.return_to_menu()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to defaults?"):
            self.settings = self.default_settings.copy()
            self.update_ui_from_settings()
            messagebox.showinfo("Settings Reset", "All settings have been reset to defaults.")
    
    def update_ui_from_settings(self):
        """Update UI controls from current settings"""
        self.target_score_var.set(str(self.settings['target_score']))
        self.animation_speed_var.set(self.settings['animation_speed'])
        self.sound_enabled_var.set(self.settings['sound_enabled'])
        self.auto_play_var.set(self.settings['auto_play_stock'])
        self.card_hints_var.set(self.settings['show_card_hints'])
        self.theme_var.set(self.settings['theme'])
        self.ai_difficulty_var.set(self.settings['ai_difficulty'])
        self.confirm_actions_var.set(self.settings['confirm_actions'])
        self.strategy_tips_var.set(self.settings['show_strategy_tips'])
        self.card_back_color = self.settings['card_back_color']
        self.color_preview.config(bg=self.card_back_color)
    
    def export_settings(self):
        """Export settings to a file"""
        if not self.save_current_settings():
            return
        
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            title="Export Settings",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.settings, f, indent=2)
                messagebox.showinfo("Export Successful", f"Settings exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export settings: {e}")
    
    def import_settings(self):
        """Import settings from a file"""
        from tkinter import filedialog
        
        filename = filedialog.askopenfilename(
            title="Import Settings",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    imported_settings = json.load(f)
                
                # Validate imported settings
                valid_settings = self.default_settings.copy()
                valid_settings.update(imported_settings)
                
                self.settings = valid_settings
                self.update_ui_from_settings()
                
                messagebox.showinfo("Import Successful", "Settings imported successfully!")
                
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import settings: {e}")
    
    def return_to_menu(self):
        """Return to main menu"""
        self.main_window.show_menu_screen()
    
    def destroy(self):
        """Destroy the settings screen"""
        if self.frame:
            self.frame.destroy()