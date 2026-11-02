"""
Enhanced action selection dialog for cards with multiple options
Features improved UI, strategy hints, and better user experience
FIXED: Button visibility issue by adjusting dialog size and layout
"""

import tkinter as tk
from tkinter import ttk

class ActionDialog:
    """Enhanced dialog for selecting card action when multiple options available"""
    
    def __init__(self, parent, card, options):
        """Initialize enhanced action dialog"""
        self.parent = parent
        self.card = card
        self.options = options
        self.result = None
        self.selected_index = 0
        
        # Calculate dynamic height based on number of options
        base_height = 280
        option_height = 60  # Height per option
        max_options_height = 200  # Maximum height for options area
        calculated_height = base_height + min(len(options) * option_height, max_options_height)
        dialog_height = min(calculated_height, 600)  # Cap at 600px
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Choose Action - {card}")
        self.dialog.geometry(f"480x{dialog_height}")  # Made wider and dynamic height
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Configure dialog appearance
        self.dialog.configure(bg='#1a2332')
        
        # Center dialog
        self.center_dialog()
        
        # Create dialog content
        self.create_dialog_content()
        
        # Set up keyboard navigation
        self.setup_keyboard_navigation()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def center_dialog(self):
        """Center dialog on parent window"""
        self.dialog.update_idletasks()
        
        # Get parent window position and size
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Calculate dialog position
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
    
    def create_dialog_content(self):
        """Create enhanced dialog content with better layout"""
        # Main frame with gradient effect
        main_frame = tk.Frame(self.dialog, bg='#1a2332')
        main_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Header with card information
        self.create_header(main_frame)
        
        # Options selection area (with controlled height)
        self.create_options_area(main_frame)
        
        # Action buttons (always at bottom)
        self.create_buttons(main_frame)
    
    def create_header(self, parent):
        """Create enhanced dialog header"""
        header_frame = tk.Frame(parent, bg='#2a3b4c', relief='raised', bd=2)
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Header content
        header_content = tk.Frame(header_frame, bg='#2a3b4c', padx=15, pady=8)
        header_content.pack(fill='x')
        
        # Title with icon
        title_frame = tk.Frame(header_content, bg='#2a3b4c')
        title_frame.pack(fill='x')
        
        # Card icon
        card_icon = tk.Label(
            title_frame,
            text="🎴",
            font=('Arial', 18),
            fg='#4a9eff',
            bg='#2a3b4c'
        )
        card_icon.pack(side='left')
        
        # Title text
        title_label = tk.Label(
            title_frame,
            text="Choose Your Move",
            font=('Arial', 14, 'bold'),
            fg='#ffffff',
            bg='#2a3b4c'
        )
        title_label.pack(side='left', padx=(10, 0))
        
        # Card info
        card_info = tk.Label(
            header_content,
            text=f"Playing: {self.card} {self.card.get_suit_symbol()}",
            font=('Arial', 11, 'bold'),
            fg='#7db8ff',
            bg='#2a3b4c'
        )
        card_info.pack(pady=(5, 0))
    
    def create_options_area(self, parent):
        """Create enhanced options selection area with scrolling if needed"""
        options_frame = tk.LabelFrame(
            parent,
            text=" Available Actions ",
            font=('Arial', 10, 'bold'),
            fg='#4a9eff',
            bg='#1a2332',
            padx=8,
            pady=6
        )
        options_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # If many options, add scrolling
        if len(self.options) > 4:
            # Create canvas and scrollbar for scrolling
            canvas = tk.Canvas(options_frame, bg='#1a2332', highlightthickness=0)
            scrollbar = tk.Scrollbar(options_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#1a2332')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            options_container = scrollable_frame
        else:
            # Direct container for few options
            options_container = tk.Frame(options_frame, bg='#1a2332')
            options_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create option buttons
        self.option_buttons = []
        
        for i, option in enumerate(self.options):
            self.create_option_button(options_container, option, i)
        
        # Select first option by default
        if self.options:
            self.select_option(0)
    
    def create_option_button(self, parent, option, index):
        """Create an enhanced option button"""
        # Option frame
        option_frame = tk.Frame(parent, bg='#2d3e52', relief='raised', bd=1)
        option_frame.pack(fill='x', pady=2, padx=3)
        
        # Option button
        btn = tk.Button(
            option_frame,
            text=option['description'],
            font=('Arial', 9, 'bold'),
            fg='#ffffff',
            bg='#3d4e62',
            activebackground='#4a9eff',
            activeforeground='#ffffff',
            relief='flat',
            bd=0,
            padx=10,
            pady=6,
            anchor='w',
            command=lambda idx=index: self.select_option(idx),
            wraplength=400
        )
        btn.pack(fill='x', padx=3, pady=2)
        
        # Add strategic indicator
        strategy_indicator = self.get_strategy_indicator(option)
        if strategy_indicator:
            strategy_label = tk.Label(
                option_frame,
                text=strategy_indicator,
                font=('Arial', 7, 'bold'),
                fg=self.get_strategy_color(option),
                bg='#2d3e52'
            )
            strategy_label.pack(anchor='e', padx=6, pady=(0, 2))
        
        self.option_buttons.append((btn, option_frame))
        
        # Hover effects
        def on_enter(e, idx=index):
            if idx != self.selected_index:
                btn.config(bg='#4d5e72')
                option_frame.config(bg='#3d4e62')
        
        def on_leave(e, idx=index):
            if idx != self.selected_index:
                btn.config(bg='#3d4e62')
                option_frame.config(bg='#2d3e52')
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
    
    def get_strategy_indicator(self, option):
        """Get strategy indicator for an option"""
        new_count = option.get('new_count', 0)
        
        if new_count == 0:
            return "🏆 WINNING!"
        elif new_count == 1:
            return "⭐ EXCELLENT"
        elif new_count in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
            return "⚡ STRATEGIC"
        elif new_count <= 10:
            return "✓ GOOD"
        elif option.get('action') == 'divide' and 'MANDATORY' in option.get('description', ''):
            return "🔒 REQUIRED"
        else:
            return "✓ VALID"
    
    def get_strategy_color(self, option):
        """Get color for strategy indicator"""
        new_count = option.get('new_count', 0)
        
        if new_count == 0:
            return "#00ff00"  # Green
        elif new_count <= 3:
            return "#4a9eff"  # Blue
        elif new_count <= 10:
            return "#ffaa00"  # Orange
        elif 'MANDATORY' in option.get('description', ''):
            return "#ff6b6b"  # Red
        else:
            return "#a0b4c8"  # Gray
    
    def select_option(self, index):
        """Select an option and update UI"""
        try:
            # Deselect previous option
            if hasattr(self, 'selected_index') and hasattr(self, 'option_buttons'):
                if 0 <= self.selected_index < len(self.option_buttons):
                    old_btn, old_frame = self.option_buttons[self.selected_index]
                    old_btn.config(bg='#3d4e62')
                    old_frame.config(bg='#2d3e52')
            
            # Select new option
            if 0 <= index < len(self.option_buttons):
                self.selected_index = index
                btn, frame = self.option_buttons[index]
                btn.config(bg='#4a9eff')
                frame.config(bg='#4a6b9e')
        except (IndexError, AttributeError, tk.TclError):
            # If there's an error, at least set the selected index
            if 0 <= index < len(self.options):
                self.selected_index = index
    
    def create_buttons(self, parent):
        """Create enhanced action buttons - FIXED: Always visible at bottom"""
        button_frame = tk.Frame(parent, bg='#1a2332')
        button_frame.pack(side='bottom', fill='x', pady=(5, 0))
        
        # Button styling
        button_style = {
            'font': ('Arial', 10, 'bold'),
            'relief': 'flat',
            'bd': 0,
            'padx': 18,
            'pady': 8,
            'cursor': 'hand2'
        }
        
        # Confirm button
        confirm_btn = tk.Button(
            button_frame,
            text="✓ CONFIRM MOVE",
            fg='#ffffff',
            bg='#28a745',
            activebackground='#218838',
            activeforeground='#ffffff',
            command=self.confirm_selection,
            **button_style
        )
        confirm_btn.pack(side='right', padx=(8, 0))
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="✕ CANCEL",
            fg='#ffffff',
            bg='#dc3545',
            activebackground='#c82333',
            activeforeground='#ffffff',
            command=self.cancel,
            **button_style
        )
        cancel_btn.pack(side='right')
        
        # Hover effects for buttons
        def create_hover_effect(button, normal_color, hover_color):
            def on_enter(e):
                button.config(bg=hover_color)
            def on_leave(e):
                button.config(bg=normal_color)
            button.bind('<Enter>', on_enter)
            button.bind('<Leave>', on_leave)
        
        create_hover_effect(confirm_btn, '#28a745', '#34ce57')
        create_hover_effect(cancel_btn, '#dc3545', '#e74c3c')
    
    def setup_keyboard_navigation(self):
        """Setup keyboard navigation for better UX"""
        try:
            # Bind keyboard shortcuts
            self.dialog.bind('<Return>', lambda e: self.confirm_selection())
            self.dialog.bind('<Escape>', lambda e: self.cancel())
            
            # Arrow key navigation
            self.dialog.bind('<Up>', lambda e: self.navigate_options(-1))
            self.dialog.bind('<Down>', lambda e: self.navigate_options(1))
            self.dialog.bind('<Key-1>', lambda e: self.select_option(0) if len(self.options) > 0 else None)
            self.dialog.bind('<Key-2>', lambda e: self.select_option(1) if len(self.options) > 1 else None)
            self.dialog.bind('<Key-3>', lambda e: self.select_option(2) if len(self.options) > 2 else None)
            
            # Focus on dialog for keyboard events
            self.dialog.focus_set()
        except tk.TclError:
            pass
    
    def navigate_options(self, direction):
        """Navigate options with arrow keys"""
        try:
            new_index = self.selected_index + direction
            if 0 <= new_index < len(self.options):
                self.select_option(new_index)
        except (AttributeError, IndexError):
            pass
    
    def confirm_selection(self):
        """Confirm the selected option"""
        try:
            if 0 <= self.selected_index < len(self.options):
                self.result = self.options[self.selected_index]
            elif self.options:
                # Fallback - select first option if nothing properly selected
                self.result = self.options[0]
                self.selected_index = 0
            
            if self.result:
                self.dialog.destroy()
        except (IndexError, AttributeError):
            # If there's any error, just select the first option as fallback
            if self.options:
                self.result = self.options[0]
                self.dialog.destroy()
    
    def cancel(self):
        """Cancel the dialog"""
        self.result = None
        try:
            self.dialog.destroy()
        except tk.TclError:
            pass