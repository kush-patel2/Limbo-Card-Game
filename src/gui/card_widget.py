"""
Enhanced card widget for displaying individual cards in the GUI
Features improved visual design, realistic card appearance, and better user feedback
"""

import tkinter as tk
from tkinter import ttk

class CardWidget(tk.Frame):
    """Enhanced widget for displaying a playing card with realistic appearance"""
    
    def __init__(self, parent, card, face_up=True, clickable=False, click_callback=None):
        """Initialize enhanced card widget"""
        # Safely get parent background color
        try:
            parent_bg = parent['bg']
        except (KeyError, tk.TclError):
            parent_bg = '#4a7c59'  # Default fallback color
        
        super().__init__(parent, bg=parent_bg, relief='flat', bd=0)
        
        self.card = card
        self.face_up = face_up
        self.clickable = clickable
        self.click_callback = click_callback
        self.selected = False
        self.hovered = False
        self.playable = True
        
        # Enhanced card dimensions for more realistic proportions
        self.card_width = 95
        self.card_height = 140
        
        # Animation variables - initialize properly
        self.animation_id = None
        self.scale_factor = 1.0
        
        self.create_card()
        self.setup_events()
    
    def create_card(self):
        """Create the enhanced realistic card display"""
        # Outer frame for 3D shadow effect
        self.shadow_frame = tk.Frame(
            self,
            width=self.card_width + 6,
            height=self.card_height + 6,
            bg='#333333',
            relief='flat',
            bd=0
        )
        self.shadow_frame.pack(padx=3, pady=3)
        self.shadow_frame.pack_propagate(False)
        
        # Main card frame with realistic rounded appearance
        self.card_frame = tk.Frame(
            self.shadow_frame,
            width=self.card_width,
            height=self.card_height,
            relief='raised',
            bd=3,
            bg='#ffffff' if self.face_up else '#1a4d72'
        )
        self.card_frame.pack(padx=3, pady=3)
        self.card_frame.pack_propagate(False)
        
        # Add subtle inner border for realism
        if self.face_up:
            inner_border = tk.Frame(
                self.card_frame,
                bg='#f0f0f0',
                relief='sunken',
                bd=1
            )
            inner_border.place(x=2, y=2, width=self.card_width-4, height=self.card_height-4)
        
        if self.face_up:
            self.create_face_up_card()
        else:
            self.create_face_down_card()
    
    def create_face_up_card(self):
        """Create realistic face-up card display"""
        # Card background
        self.card_frame.config(bg='#fafafa')
        
        # Subtle card border with suit color accent
        border_frame = tk.Frame(
            self.card_frame,
            bg=self.card.get_suit_color(),
            relief='flat',
            bd=0
        )
        border_frame.place(x=1, y=1, width=self.card_width-2, height=self.card_height-2)
        
        # White card content area
        content_frame = tk.Frame(
            border_frame,
            bg='#ffffff',
            relief='flat',
            bd=0
        )
        content_frame.place(x=1, y=1, width=self.card_width-4, height=self.card_height-4)
        
        # Top-left corner (rank and suit)
        self.create_corner_elements(content_frame, 'top_left')
        
        # Bottom-right corner (rank and suit, rotated)
        self.create_corner_elements(content_frame, 'bottom_right')
        
        # Center design
        self.create_center_design(content_frame)
        
        # Card effect indicator for special cards
        if self.card.is_face_card() or self.card.is_ace():
            self.create_special_indicator(content_frame)
    
    def create_corner_elements(self, parent, position):
        """Create corner rank and suit elements"""
        if position == 'top_left':
            x, y = 8, 8
            anchor = 'nw'
        else:  # bottom_right
            x, y = self.card_width - 16, self.card_height - 35
            anchor = 'se'
        
        # Rank
        rank_label = tk.Label(
            parent,
            text=self.card.rank,
            font=('Arial Black', 16, 'bold'),
            fg=self.card.get_suit_color(),
            bg='#ffffff',
            anchor=anchor
        )
        if position == 'top_left':
            rank_label.place(x=x, y=y)
        else:
            rank_label.place(x=x, y=y)
        
        # Suit symbol
        suit_label = tk.Label(
            parent,
            text=self.card.get_suit_symbol(),
            font=('Arial', 12, 'bold'),
            fg=self.card.get_suit_color(),
            bg='#ffffff',
            anchor=anchor
        )
        if position == 'top_left':
            suit_label.place(x=x+2, y=y+20)
        else:
            suit_label.place(x=x-2, y=y-20)
    
    def create_center_design(self, parent):
        """Create center card design"""
        center_x = self.card_width // 2
        center_y = self.card_height // 2
        
        if self.card.is_number_card():
            # Large suit symbol for number cards
            center_suit = tk.Label(
                parent,
                text=self.card.get_suit_symbol(),
                font=('Arial', 36, 'bold'),
                fg=self.card.get_suit_color(),
                bg='#ffffff'
            )
            center_suit.place(x=center_x, y=center_y-15, anchor='center')
            
            # Number value
            value_label = tk.Label(
                parent,
                text=str(self.card.get_value()),
                font=('Arial', 28, 'bold'),
                fg=self.card.get_suit_color(),
                bg='#ffffff'
            )
            value_label.place(x=center_x, y=center_y-45, anchor='center')
            
        elif self.card.is_ace():
            # Large A for Aces
            ace_label = tk.Label(
                parent,
                text="A",
                font=('Arial Black', 48, 'bold'),
                fg=self.card.get_suit_color(),
                bg='#ffffff'
            )
            ace_label.place(x=center_x, y=center_y-10, anchor='center')
            
            # Small suit symbol
            suit_small = tk.Label(
                parent,
                text=self.card.get_suit_symbol(),
                font=('Arial', 20, 'bold'),
                fg=self.card.get_suit_color(),
                bg='#ffffff'
            )
            suit_small.place(x=center_x, y=center_y+25, anchor='center')
            
        elif self.card.is_face_card():
            # Face card letter
            face_letter = tk.Label(
                parent,
                text=self.card.rank,
                font=('Arial Black', 40, 'bold'),
                fg=self.card.get_suit_color(),
                bg='#ffffff'
            )
            face_letter.place(x=center_x, y=center_y-10, anchor='center')
            
            # Decorative border for face cards
            face_border = tk.Frame(
                parent,
                bg=self.card.get_suit_color(),
                relief='raised',
                bd=1
            )
            face_border.place(x=center_x-25, y=center_y-30, width=50, height=60)
            
            # White background inside border
            face_bg = tk.Frame(
                face_border,
                bg='#ffffff'
            )
            face_bg.place(x=2, y=2, width=46, height=56)
            
            # Re-place the letter on top
            face_letter.lift()
    
    def create_special_indicator(self, parent):
        """Create special indicator for face cards and aces"""
        indicator_text = self._get_special_card_text()
        if indicator_text:
            indicator = tk.Label(
                parent,
                text=indicator_text,
                font=('Arial', 7, 'bold'),
                fg=self.card.get_suit_color(),
                bg='#f0f0f0',
                relief='flat',
                bd=1
            )
            indicator.place(x=self.card_width//2, y=self.card_height-20, anchor='center')
    
    def create_face_down_card(self):
        """Create enhanced face-down card display"""
        self.card_frame.config(bg='#1a4d72')
        
        # Create elegant pattern background
        pattern_frame = tk.Frame(
            self.card_frame,
            bg='#2a5d82',
            relief='raised',
            bd=2
        )
        pattern_frame.place(x=4, y=4, width=self.card_width-8, height=self.card_height-8)
        
        # Inner decorative pattern
        inner_pattern = tk.Frame(
            pattern_frame,
            bg='#3a6d92',
            relief='sunken',
            bd=1
        )
        inner_pattern.place(x=8, y=8, width=self.card_width-24, height=self.card_height-24)
        
        # Diamond pattern grid
        for i in range(2):
            for j in range(3):
                x = 18 + i * 22
                y = 25 + j * 28
                diamond = tk.Label(
                    inner_pattern,
                    text='♦',
                    font=('Arial', 14, 'bold'),
                    fg='#ffeb3b',
                    bg='#3a6d92'
                )
                diamond.place(x=x, y=y)
        
        # Center LIMBO logo
        logo_frame = tk.Frame(
            inner_pattern,
            bg='#ffeb3b',
            relief='raised',
            bd=1
        )
        logo_frame.place(x=self.card_width//2-25, y=self.card_height//2-15, width=50, height=30)
        
        logo_label = tk.Label(
            logo_frame,
            text='LIMBO',
            font=('Arial Black', 8, 'bold'),
            fg='#1a4d72',
            bg='#ffeb3b'
        )
        logo_label.place(relx=0.5, rely=0.5, anchor='center')
    
    def _get_special_card_text(self):
        """Get descriptive text for special cards"""
        if self.card.rank == 'A':
            return "1 or 11"
        elif self.card.rank == 'J':
            return "REPEAT"
        elif self.card.rank == 'Q':
            return "REVERSE"
        elif self.card.rank == 'K':
            return "DIVIDE"
        return ""
    
    def setup_events(self):
        """Setup enhanced mouse events"""
        if self.clickable:
            self._bind_events_recursive(self.card_frame)
            self._bind_events_recursive(self)
    
    def _bind_events_recursive(self, widget):
        """Bind events to widget and all children"""
        if self.clickable:
            widget.bind('<Button-1>', self.on_click)
            widget.bind('<Enter>', self.on_enter)
            widget.bind('<Leave>', self.on_leave)
            widget.bind('<Button-3>', self.show_tooltip)  # Right-click for tooltip
        
        for child in widget.winfo_children():
            self._bind_events_recursive(child)
    
    def on_click(self, event):
        """Handle enhanced card click with animation"""
        if self.clickable and self.click_callback:
            self.animate_click()
            self.click_callback()
    
    def on_enter(self, event):
        """Handle mouse enter with smooth hover effect"""
        if self.clickable and self.playable:
            self.hovered = True
            self.animate_hover(True)
    
    def on_leave(self, event):
        """Handle mouse leave"""
        if self.clickable:
            self.hovered = False
            self.animate_hover(False)
    
    def animate_click(self):
        """Animate card click with scale effect"""
        try:
            if hasattr(self, 'animation_id') and self.animation_id:
                self.after_cancel(self.animation_id)
        except (AttributeError, tk.TclError):
            pass
        
        try:
            # Quick scale down and back up
            self.card_frame.config(relief='sunken', bd=1)
            self.animation_id = self.after(100, lambda: self.card_frame.config(relief='raised', bd=3))
        except (AttributeError, tk.TclError):
            pass
    
    def animate_hover(self, entering):
        """Animate hover effect with smooth transitions"""
        if entering and self.playable:
            # Bright glow effect
            self.shadow_frame.config(bg='#4a9eff')
            self.card_frame.config(relief='raised', bd=4)
            # Slight lift effect
            self.pack_configure(pady=1)
        else:
            # Normal appearance
            self.shadow_frame.config(bg='#333333')
            self.card_frame.config(relief='raised', bd=3)
            self.pack_configure(pady=3)
        
        self.update_appearance()
    
    def set_selected(self, selected):
        """Set card selection state with visual feedback"""
        self.selected = selected
        self.update_appearance()
    
    def set_playable(self, playable):
        """Set whether card is playable with visual indication"""
        self.playable = playable
        self.update_appearance()
    
    def set_clickable(self, clickable):
        """Enable/disable card clicking"""
        self.clickable = clickable
        if clickable:
            self.setup_events()
        else:
            self._unbind_events_recursive(self.card_frame)
            self._unbind_events_recursive(self)
        self.update_appearance()
    
    def _unbind_events_recursive(self, widget):
        """Unbind events from widget and children"""
        try:
            widget.unbind('<Button-1>')
            widget.unbind('<Enter>')
            widget.unbind('<Leave>')
            widget.unbind('<Button-3>')
        except tk.TclError:
            pass
        
        for child in widget.winfo_children():
            self._unbind_events_recursive(child)
    
    def update_appearance(self):
        """Update card appearance based on state"""
        if self.selected:
            # Selected state - bright green glow
            self.shadow_frame.config(bg='#00ff44')
            self.card_frame.config(highlightbackground='#00ff44', highlightthickness=3)
        elif self.hovered and self.clickable and self.playable:
            # Hovered state - blue glow (handled in animate_hover)
            pass
        elif not self.playable and self.face_up:
            # Unplayable state - red tint
            self.shadow_frame.config(bg='#ff4444')
            self.card_frame.config(highlightbackground='#ff4444', highlightthickness=2)
        else:
            # Normal state
            self.shadow_frame.config(bg='#333333')
            self.card_frame.config(highlightthickness=0)
    
    def highlight_playable(self, playable=True):
        """Highlight card as playable or not with enhanced visuals"""
        self.set_playable(playable)
        
        if playable:
            # Green pulsing border for playable cards
            self.shadow_frame.config(bg='#00ff44')
            self.animate_pulse(True)
        else:
            # Red border for unplayable cards
            self.shadow_frame.config(bg='#ff4444')
    
    def animate_pulse(self, active):
        """Create subtle pulsing animation for playable cards"""
        if active and self.playable and not self.selected:
            try:
                # Subtle glow pulse
                colors = ['#00ff44', '#00cc33', '#00ff44']
                for i, color in enumerate(colors):
                    self.after(i * 400, lambda c=color: self.shadow_frame.config(bg=c) if not self.selected else None)
                # Repeat pulse
                self.after(1200, lambda: self.animate_pulse(True))
            except (AttributeError, tk.TclError):
                pass
    
    def clear_highlight(self):
        """Clear any highlighting effects"""
        self.shadow_frame.config(bg='#333333')
        self.card_frame.config(highlightthickness=0)
        self.set_playable(True)
    
    def show_tooltip(self, event):
        """Show enhanced tooltip with card information"""
        if not self.face_up:
            return
        
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+15}+{event.y_root+10}")
        tooltip.configure(bg='#2a3b4c')
        
        # Tooltip frame
        frame = tk.Frame(tooltip, bg='#2a3b4c', relief='solid', bd=2)
        frame.pack(padx=5, pady=5)
        
        # Card name
        name_label = tk.Label(
            frame,
            text=str(self.card),
            font=('Arial', 12, 'bold'),
            fg='#ffffff',
            bg='#2a3b4c'
        )
        name_label.pack(pady=(5, 0))
        
        # Card effect description
        effect = self.get_card_effect_description()
        if effect:
            effect_label = tk.Label(
                frame,
                text=effect,
                font=('Arial', 9),
                fg='#a0b4c8',
                bg='#2a3b4c',
                justify='left',
                wraplength=200
            )
            effect_label.pack(pady=5)
        
        # Auto-hide tooltip
        tooltip.after(3000, tooltip.destroy)
    
    def get_card_effect_description(self):
        """Get detailed description of card effects"""
        if self.card.is_number_card():
            value = self.card.get_value()
            return f"• Divide by {value} (if possible)\n• Otherwise subtract {value}\n• Division is MANDATORY when possible"
        elif self.card.is_ace():
            return "• Subtract 1 OR 11 (your choice)\n• Cannot divide\n• Very flexible for precise control"
        elif self.card.rank == 'J':
            return "• Repeats the effect of the previous card\n• Copies exact same action"
        elif self.card.rank == 'Q':
            return "• Reverses the digits of current count\n• Only if reversal reduces the count"
        elif self.card.rank == 'K':
            return "• Divide by ANY number you choose\n• Must divide evenly (no remainder)"
        
        return "Click to play this card"
    
    def destroy(self):
        """Clean up card widget"""
        try:
            if hasattr(self, 'animation_id') and self.animation_id:
                self.after_cancel(self.animation_id)
        except (AttributeError, tk.TclError):
            pass
        try:
            super().destroy()
        except tk.TclError:
            pass