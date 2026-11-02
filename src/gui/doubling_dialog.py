"""
Doubling dialog for Limbo Card Game GUI
Handles the doubling/redoubling phase before each round
"""

import tkinter as tk
from tkinter import ttk

class DoublingDialog:
    """Dialog for handling doubling and redoubling decisions"""
    
    def __init__(self, parent, player_name, is_redouble=False, current_multiplier=1):
        """Initialize doubling dialog"""
        self.parent = parent
        self.player_name = player_name
        self.is_redouble = is_redouble
        self.current_multiplier = current_multiplier
        self.result = None  # True = double, False = no double
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Doubling Decision")
        self.dialog.geometry("450x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Configure dialog appearance
        self.dialog.configure(bg='#1a2332')
        
        # Center dialog
        self.center_dialog()
        
        # Create dialog content
        self.create_dialog_content()
        
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
        dialog_width = 450
        dialog_height = 300
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
    
    def create_dialog_content(self):
        """Create dialog content"""
        # Main frame
        main_frame = tk.Frame(self.dialog, bg='#1a2332', padx=20, pady=15)
        main_frame.pack(fill='both', expand=True)
        
        # Header
        self.create_header(main_frame)
        
        # Content
        self.create_content(main_frame)
        
        # Buttons
        self.create_buttons(main_frame)
    
    def create_header(self, parent):
        """Create dialog header"""
        header_frame = tk.Frame(parent, bg='#2a3b4c', relief='raised', bd=2)
        header_frame.pack(fill='x', pady=(0, 15))
        
        header_content = tk.Frame(header_frame, bg='#2a3b4c', padx=15, pady=10)
        header_content.pack(fill='x')
        
        # Title
        if self.is_redouble:
            title = "REDOUBLE DECISION"
            icon = "⚡"
        else:
            title = "DOUBLE DECISION"
            icon = "🎯"
        
        title_frame = tk.Frame(header_content, bg='#2a3b4c')
        title_frame.pack()
        
        # Icon
        icon_label = tk.Label(
            title_frame,
            text=icon,
            font=('Arial', 24),
            fg='#4a9eff',
            bg='#2a3b4c'
        )
        icon_label.pack(side='left')
        
        # Title text
        title_label = tk.Label(
            title_frame,
            text=title,
            font=('Arial', 16, 'bold'),
            fg='#ffffff',
            bg='#2a3b4c'
        )
        title_label.pack(side='left', padx=(10, 0))
        
        # Player name
        player_label = tk.Label(
            header_content,
            text=f"{self.player_name}'s Decision",
            font=('Arial', 12, 'bold'),
            fg='#7db8ff',
            bg='#2a3b4c'
        )
        player_label.pack(pady=(8, 0))
    
    def create_content(self, parent):
        """Create dialog content"""
        content_frame = tk.Frame(parent, bg='#1a2332')
        content_frame.pack(fill='both', expand=True, pady=15)
        
        # Current stakes
        stakes_frame = tk.LabelFrame(
            content_frame,
            text=" Current Stakes ",
            font=('Arial', 11, 'bold'),
            fg='#4a9eff',
            bg='#1a2332',
            padx=10,
            pady=8
        )
        stakes_frame.pack(fill='x', pady=(0, 15))
        
        current_label = tk.Label(
            stakes_frame,
            text=f"Current Multiplier: {self.current_multiplier}x",
            font=('Arial', 12, 'bold'),
            fg='#ffffff',
            bg='#1a2332'
        )
        current_label.pack()
        
        # Decision explanation
        if self.is_redouble:
            new_multiplier = self.current_multiplier * 2
            explanation = f"""The stakes have been doubled to {self.current_multiplier}x.

You can REDOUBLE to increase the stakes to {new_multiplier}x.

If you redouble and win the round, you'll get {new_multiplier} times 
the normal points. If you lose, your opponent gets 
{new_multiplier} times their normal points.

Choose wisely based on your hand strength!"""
        else:
            new_multiplier = 2
            explanation = f"""You can DOUBLE the stakes for this round.

If you double and win, you'll get {new_multiplier} times the normal points.
If you double and lose, your opponent gets normal points.

The dealer will then have the option to redouble (4x stakes).

Consider your hand strength before deciding!"""
        
        explanation_label = tk.Label(
            content_frame,
            text=explanation,
            font=('Arial', 10),
            fg='#e0e0e0',
            bg='#1a2332',
            justify='left',
            wraplength=400
        )
        explanation_label.pack(pady=10)
    
    def create_buttons(self, parent):
        """Create action buttons"""
        button_frame = tk.Frame(parent, bg='#1a2332')
        button_frame.pack(fill='x', pady=(15, 0))
        
        # Button styling
        button_style = {
            'font': ('Arial', 12, 'bold'),
            'relief': 'raised',
            'bd': 2,
            'padx': 25,
            'pady': 10,
            'cursor': 'hand2'
        }
        
        # Double/Redouble button
        action_text = "REDOUBLE" if self.is_redouble else "DOUBLE"
        new_multiplier = self.current_multiplier * 2
        
        double_btn = tk.Button(
            button_frame,
            text=f"🎲 {action_text} ({new_multiplier}x)",
            fg='#ffffff',
            bg='#dc3545',
            activebackground='#c82333',
            activeforeground='#ffffff',
            command=self.accept_double,
            **button_style
        )
        double_btn.pack(side='left', padx=(0, 15))
        
        # No double button
        no_double_btn = tk.Button(
            button_frame,
            text="❌ NO DOUBLE",
            fg='#ffffff',
            bg='#28a745',
            activebackground='#218838',
            activeforeground='#ffffff',
            command=self.decline_double,
            **button_style
        )
        no_double_btn.pack(side='left')
        
        # Hover effects
        def create_hover_effect(button, normal_color, hover_color):
            def on_enter(e):
                button.config(bg=hover_color)
            def on_leave(e):
                button.config(bg=normal_color)
            button.bind('<Enter>', on_enter)
            button.bind('<Leave>', on_leave)
        
        create_hover_effect(double_btn, '#dc3545', '#e74c3c')
        create_hover_effect(no_double_btn, '#28a745', '#34ce57')
        
        # Keyboard shortcuts
        self.dialog.bind('<Return>', lambda e: self.decline_double())  # Enter = No double (safer default)
        self.dialog.bind('<Escape>', lambda e: self.decline_double())
        self.dialog.bind('<d>', lambda e: self.accept_double())
        self.dialog.bind('<D>', lambda e: self.accept_double())
        
        # Focus for keyboard events
        self.dialog.focus_set()
    
    def accept_double(self):
        """Accept the doubling"""
        self.result = True
        self.dialog.destroy()
    
    def decline_double(self):
        """Decline the doubling"""
        self.result = False
        self.dialog.destroy()


class DoublingPhaseHandler:
    """Handles the entire doubling phase for both players"""
    
    def __init__(self, parent, game_manager):
        """Initialize doubling phase handler"""
        self.parent = parent
        self.game_manager = game_manager
        self.completed = False
    
    def start_doubling_phase(self):
        """Start the doubling phase"""
        # Non-dealer goes first
        non_dealer_index = (self.game_manager.dealer_index + 1) % 2
        dealer_index = self.game_manager.dealer_index
        
        non_dealer = self.game_manager.get_player(non_dealer_index)
        dealer = self.game_manager.get_player(dealer_index)
        
        # Non-dealer's doubling decision
        if non_dealer.is_human:
            dialog = DoublingDialog(self.parent, non_dealer.name)
            wants_double = dialog.result
        else:
            # AI decision
            game_state = self.game_manager.get_game_state()
            wants_double = non_dealer.should_double(1, game_state)
        
        if wants_double:
            # Non-dealer doubled, now dealer can redouble
            self.game_manager.handle_doubling(non_dealer_index, True)
            
            # Dealer's redoubling decision
            if dealer.is_human:
                dialog = DoublingDialog(self.parent, dealer.name, is_redouble=True, current_multiplier=2)
                wants_redouble = dialog.result
            else:
                # AI decision
                game_state = self.game_manager.get_game_state()
                wants_redouble = dealer.should_double(2, game_state)
            
            self.game_manager.handle_doubling(dealer_index, wants_redouble)
        else:
            # Non-dealer declined, no doubling
            self.game_manager.handle_doubling(non_dealer_index, False)
        
        self.completed = True
        return True