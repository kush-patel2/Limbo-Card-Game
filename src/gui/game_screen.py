"""Main game screen for Limbo GUI game with complete rule implementation."""

import tkinter as tk
from tkinter import ttk, messagebox

from .card_widget import CardWidget
from .action_dialog import ActionDialog


class GameScreen:
    """Main game screen displaying the active game with complete Limbo rules."""

    def __init__(self, parent: tk.Widget, main_window, game_mode: str):
        """Create the game screen and start the first round."""
        self.parent = parent
        self.main_window = main_window
        self.game_mode = game_mode
        self.game_manager = main_window.get_game_manager()

        # GUI state
        self.card_widgets = {}
        self.selected_card = None  # (player_index, card_index)
        self.animation_active = False
        self.widgets_destroyed = False  # Track widget destruction

        # Build UI first (so callbacks can safely update widgets)
        self._create_screen()

        # Register callbacks *after* widgets exist
        self._setup_game_callbacks()

        # Start with proper doubling phase
        self.game_manager.start_new_round()

    def _create_screen(self):
        """Create and lay out all UI sections with improved sizing."""
        # Use a more appealing background color
        self.frame = tk.Frame(self.parent, bg="#2e5c3e")  # Forest green
        self.frame.pack(fill="both", expand=True)

        # Create main game area and side panel with improved sizing
        self._create_main_container()
        self._create_side_panel()      # Side panel first
        self._create_game_area()       # Game area second

    def _create_main_container(self):
        """Create the main container with proper 3:1 ratio layout."""
        # Main container using grid for better control
        self.main_container = tk.Frame(self.frame, bg="#2e5c3e")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid weights for 3:1 ratio
        self.main_container.grid_columnconfigure(0, weight=3)  # Game area gets 3x space
        self.main_container.grid_columnconfigure(1, weight=1)  # Side panel gets 1x space
        self.main_container.grid_rowconfigure(0, weight=1)

    def _create_game_area(self):
        """Create the main game area (3/4 of screen)."""
        self.game_area = tk.Frame(self.main_container, bg="#2e5c3e")
        self.game_area.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Configure game area grid
        self.game_area.grid_rowconfigure(0, weight=1)  # Top area (opponent)
        self.game_area.grid_rowconfigure(1, weight=1)  # Center area (game state)
        self.game_area.grid_rowconfigure(2, weight=1)  # Bottom area (player)
        self.game_area.grid_columnconfigure(0, weight=1)

        self._create_top_area()      # Opponent (player 2)
        self._create_center_area()   # Game state display
        self._create_bottom_area()   # Local player (player 1)

    def _create_side_panel(self):
        """Create properly sized side panel (1/4 of screen)."""
        self.side_frame = tk.Frame(self.main_container, bg="#1a3d2e", width=280, relief="raised", bd=2)
        self.side_frame.grid(row=0, column=1, sticky="nsew")
        self.side_frame.grid_propagate(False)  # Maintain fixed width

        # Compact title
        title_frame = tk.Frame(self.side_frame, bg="#1a3d2e")
        title_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(
            title_frame,
            text="Game Controls",
            font=("Arial", 14, "bold"),
            fg="#ffffff",
            bg="#1a3d2e",
        ).pack()

        # Compact sections
        self._create_compact_game_info()
        self._create_compact_action_buttons()
        self._create_compact_rules()

    def _create_compact_game_info(self):
        """Create compact game information section."""
        info_frame = tk.LabelFrame(
            self.side_frame,
            text="Game Info",
            font=("Arial", 11, "bold"),
            fg="#87ceeb",
            bg="#1a3d2e",
            padx=10,
            pady=8
        )
        info_frame.pack(fill="x", padx=10, pady=8)

        # More compact labels
        self.target_score_label = tk.Label(
            info_frame, text="Target: 200", font=("Arial", 10), 
            fg="#ffffff", bg="#1a3d2e"
        )
        self.target_score_label.pack(pady=2)

        self.round_multiplier_label = tk.Label(
            info_frame, text="Round: 1x", font=("Arial", 10), 
            fg="#ffffff", bg="#1a3d2e"
        )
        self.round_multiplier_label.pack(pady=2)

        self.deck_size_label = tk.Label(
            info_frame, text="Deck: 42 cards", font=("Arial", 10), 
            fg="#ffffff", bg="#1a3d2e"
        )
        self.deck_size_label.pack(pady=2)

        self.turn_indicator_label = tk.Label(
            info_frame, text="Your Turn", font=("Arial", 10, "bold"), 
            fg="#90ee90", bg="#1a3d2e"
        )
        self.turn_indicator_label.pack(pady=2)

    def _create_compact_action_buttons(self):
        """Create properly sized action buttons section."""
        buttons_frame = tk.LabelFrame(
            self.side_frame,
            text="Actions",
            font=("Arial", 11, "bold"),
            fg="#87ceeb",
            bg="#1a3d2e",
            padx=10,
            pady=8
        )
        buttons_frame.pack(fill="x", padx=10, pady=8)

        # Play card button
        self.play_card_button = tk.Button(
            buttons_frame,
            text="Play Selected Card",
            font=("Arial", 10, "bold"),
            bg="#4a90e2",
            fg="white",
            activebackground="#357abd",
            activeforeground="white",
            command=self.play_selected_card,
            state="disabled",
            relief="raised",
            bd=2,
            padx=10,
            pady=8,
            wraplength=200
        )
        self.play_card_button.pack(fill="x", pady=4)

        # Doubling buttons
        self.double_button = tk.Button(
            buttons_frame,
            text="Double Stakes",
            font=("Arial", 10),
            bg="#ff8c42",
            fg="white",
            activebackground="#e67e22",
            activeforeground="white",
            command=self.handle_double,
            state="disabled",
            relief="raised",
            bd=2,
            padx=10,
            pady=6,
            wraplength=200
        )
        self.double_button.pack(fill="x", pady=3)

        self.skip_doubling_button = tk.Button(
            buttons_frame,
            text="Skip Doubling",
            font=("Arial", 10),
            bg="#6c757d",
            fg="white",
            activebackground="#5a6268",
            activeforeground="white",
            command=self.skip_doubling,
            state="disabled",
            relief="raised",
            bd=2,
            padx=10,
            pady=6,
            wraplength=200
        )
        self.skip_doubling_button.pack(fill="x", pady=3)

        # Draw card button (for forced draws)
        self.draw_card_button = tk.Button(
            buttons_frame,
            text="Draw from Stock",
            font=("Arial", 10),
            bg="#dc3545",
            fg="white",
            activebackground="#c82333",
            activeforeground="white",
            command=self.draw_stock_card,
            state="disabled",
            relief="raised",
            bd=2,
            padx=10,
            pady=6,
            wraplength=200
        )
        self.draw_card_button.pack(fill="x", pady=3)

        # New round button
        self.new_round_button = tk.Button(
            buttons_frame,
            text="New Round",
            font=("Arial", 10),
            bg="#28a745",
            fg="white",
            activebackground="#218838",
            activeforeground="white",
            command=self.start_new_round,
            state="disabled",
            relief="raised",
            bd=2,
            padx=10,
            pady=6,
            wraplength=200
        )
        self.new_round_button.pack(fill="x", pady=3)

        # Main menu button
        main_menu_btn = tk.Button(
            buttons_frame,
            text="Main Menu",
            font=("Arial", 10),
            bg="#6c757d",
            fg="white",
            activebackground="#5a6268",
            activeforeground="white",
            command=self.return_to_menu,
            relief="raised",
            bd=2,
            padx=10,
            pady=6,
            wraplength=200
        )
        main_menu_btn.pack(fill="x", pady=3)

    def _create_compact_rules(self):
        """Create compact rules reference."""
        rules_frame = tk.LabelFrame(
            self.side_frame,
            text="Quick Rules",
            font=("Arial", 10, "bold"),
            fg="#87ceeb",
            bg="#1a3d2e",
            padx=8,
            pady=6
        )
        rules_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Scrollable text with proper sizing
        text_frame = tk.Frame(rules_frame, bg="#1a3d2e")
        text_frame.pack(fill="both", expand=True)

        rules_text = tk.Text(
            text_frame,
            height=8,  # Increased height
            font=("Arial", 9),  # Slightly larger font
            fg="#e0e0e0",
            bg="#2a4a3a",
            wrap="word",
            relief="sunken",
            bd=1,
            padx=5,
            pady=5
        )
        
        scrollbar = tk.Scrollbar(text_frame, command=rules_text.yview, width=15)
        rules_text.configure(yscrollcommand=scrollbar.set)
        
        rules_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Updated rules with drawing info
        rules_content = (
            "• Start at 101, reduce to 0\n"
            "• DIVISION IS MANDATORY when possible\n"
            "• Aces: subtract 1 or 11\n"
            "• Jack: repeat last card\n"
            "• Queen: reverse digits\n"
            "• King: divide by choice\n"
            "• Can't play? Draw from stock!\n"
            "• Drawn card playable? Must play!\n"
            "• Last player wins round\n\n"
            "Example: Count 96, play 6 → MUST divide (96÷6=16)"
        )

        rules_text.insert("1.0", rules_content)
        rules_text.config(state="disabled")

    def _create_top_area(self):
        """Create opponent area with enhanced layout."""
        self.top_frame = tk.Frame(self.game_area, bg="#4a7c59", height=180, relief="raised", bd=2)
        self.top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        self.top_frame.grid_propagate(False)

        # Info bar with better styling
        info = tk.Frame(self.top_frame, bg="#2d5a27", relief="flat", bd=1)
        info.pack(fill="x", padx=8, pady=8)

        self.opponent_name_label = tk.Label(
            info, text="Player 2", font=("Arial", 16, "bold"), fg="#fff", bg="#2d5a27"
        )
        self.opponent_name_label.pack(side="left", padx=15, pady=8)

        self.opponent_score_label = tk.Label(
            info, text="Score: 0", font=("Arial", 14), fg="#ddd", bg="#2d5a27"
        )
        self.opponent_score_label.pack(side="right", padx=15, pady=8)

        # Enhanced hand area
        self.opponent_hand_frame = tk.Frame(self.top_frame, bg="#4a7c59")
        self.opponent_hand_frame.pack(fill="both", expand=True, pady=8)

    def _create_center_area(self):
        """Create enhanced center game state area."""
        self.center_frame = tk.Frame(self.game_area, bg="#5a8a69", height=240, relief="sunken", bd=3)
        self.center_frame.grid(row=1, column=0, sticky="ew", pady=8)
        self.center_frame.grid_propagate(False)

        # Current count display with better layout
        count_container = tk.Frame(self.center_frame, bg="#5a8a69")
        count_container.pack(expand=True, fill="both")

        tk.Label(
            count_container,
            text="Current Count",
            font=("Arial", 22, "bold"),
            fg="#ffffff",
            bg="#5a8a69",
        ).pack(pady=(30, 10))

        self.count_label = tk.Label(
            count_container,
            text="101",
            font=("Arial", 80, "bold"),  # Extra large for visibility
            fg="#ffff00",
            bg="#5a8a69",
        )
        self.count_label.pack()

        # Enhanced info row
        info_row = tk.Frame(self.center_frame, bg="#5a8a69")
        info_row.pack(side="bottom", fill="x", pady=20)

        self.cards_played_label = tk.Label(
            info_row,
            text="Cards Played: 0",
            font=("Arial", 15),
            fg="#e0e0e0",
            bg="#5a8a69",
        )
        self.cards_played_label.pack(side="left", padx=30)

        self.last_card_label = tk.Label(
            info_row,
            text="Last Card: None",
            font=("Arial", 15),
            fg="#e0e0e0",
            bg="#5a8a69",
        )
        self.last_card_label.pack(side="right", padx=30)

        # Game status area (for doubling, drawing, etc.)
        self.status_frame = tk.Frame(self.center_frame, bg="#5a8a69")
        self.status_frame.pack(side="top", fill="x", pady=15)

        self.game_status_label = tk.Label(
            self.status_frame,
            text="",
            font=("Arial", 18, "bold"),
            fg="#ffeb3b",
            bg="#5a8a69",
        )
        self.game_status_label.pack()

    def _create_bottom_area(self):
        """Create enhanced local player area."""
        self.bottom_frame = tk.Frame(self.game_area, bg="#4a7c59", height=180, relief="raised", bd=2)
        self.bottom_frame.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        self.bottom_frame.grid_propagate(False)

        # Enhanced info bar
        info = tk.Frame(self.bottom_frame, bg="#2d5a27", relief="flat", bd=1)
        info.pack(fill="x", padx=8, pady=8)

        self.player_name_label = tk.Label(
            info, text="Player 1", font=("Arial", 16, "bold"), fg="#fff", bg="#2d5a27"
        )
        self.player_name_label.pack(side="left", padx=15, pady=8)

        self.player_score_label = tk.Label(
            info, text="Score: 0", font=("Arial", 14), fg="#ddd", bg="#2d5a27"
        )
        self.player_score_label.pack(side="right", padx=15, pady=8)

        # Enhanced hand area
        self.player_hand_frame = tk.Frame(self.bottom_frame, bg="#4a7c59")
        self.player_hand_frame.pack(fill="both", expand=True, pady=8)

    def _setup_game_callbacks(self):
        """Register game callbacks."""
        gm = self.game_manager
        gm.set_game_state_callback(self.on_game_state_changed)
        gm.set_card_played_callback(self.on_card_played)
        gm.set_round_ended_callback(self.on_round_ended)
        gm.set_game_ended_callback(self.on_game_ended)
        gm.set_card_drawn_callback(self.on_card_drawn)

    def _safe_widget_operation(self, operation, *args, **kwargs):
        """Safely perform widget operations with error handling."""
        if self.widgets_destroyed:
            return None
        try:
            return operation(*args, **kwargs)
        except tk.TclError:
            # Widget has been destroyed
            self.widgets_destroyed = True
            return None
        except Exception as e:
            print(f"Widget operation error: {e}")
            return None

    # Callback handlers
    def on_game_state_changed(self, game_state):
        """Handle game state changes."""
        if self.widgets_destroyed:
            return
            
        try:
            self._update_count_display(game_state["current_count"])
            self._update_cards_played(game_state["cards_played"])
            self._update_last_card(game_state["last_card"])
            self._update_current_player(game_state)
            self._update_deck_size(game_state["deck_size"])
            self._update_player_info(game_state["players"])
            self._update_round_multiplier(game_state["round_multiplier"])
            self._update_player_hands()
            self._update_button_states(game_state)
            self._update_game_status(game_state)
        except Exception as e:
            print(f"Error updating game state: {e}")

    def on_card_played(self, player_index, card, action_data):
        """Handle card played events."""
        if not self.widgets_destroyed:
            self._show_card_played_animation(player_index, card)

    def on_card_drawn(self, player_index, card):
        """Handle card drawn events."""
        if not self.widgets_destroyed:
            player_name = self.game_manager.get_player(player_index).name
            self._show_draw_notification(player_name, card)

    def on_round_ended(self, winner, winner_points, loser_points):
        """Handle round end."""
        if self.widgets_destroyed:
            return
            
        winner_name = winner.name
        message = f"Round Over!\n\n{winner_name} wins!\n\nPoints awarded:\n{winner_name}: {winner_points}\nOpponent: {loser_points}"
        messagebox.showinfo("Round Complete", message)
        self._safe_widget_operation(lambda: self.new_round_button.config(state="normal"))

    def on_game_ended(self, winner):
        """Handle game end."""
        if self.widgets_destroyed:
            return
            
        winner_name = winner.name
        message = f"Game Over!\n\n{winner_name} wins the game!\n\nFinal Score: {winner.score}"
        messagebox.showinfo("Game Complete", message)
        
        if messagebox.askyesno("Play Again?", "Would you like to start a new game?"):
            self.start_new_game()
        else:
            self.return_to_menu()

    def _update_count_display(self, count):
        """Update the count display with enhanced colors."""
        self._safe_widget_operation(lambda: self.count_label.config(text=str(count)))
        
        # Enhanced color coding
        if count <= 5:
            color = "#ff1111"  # Bright red - critical
        elif count <= 10:
            color = "#ff4444"  # Red - danger zone
        elif count <= 30:
            color = "#ff8844"  # Orange - caution
        else:
            color = "#ffff00"  # Yellow - normal
        
        self._safe_widget_operation(lambda: self.count_label.config(fg=color))

    def _update_cards_played(self, cards_played):
        """Update cards played display."""
        self._safe_widget_operation(lambda: self.cards_played_label.config(text=f"Cards Played: {cards_played}"))

    def _update_last_card(self, last_card):
        """Update last card display."""
        if last_card:
            text = f"Last Card: {last_card}"
        else:
            text = "Last Card: None"
        self._safe_widget_operation(lambda: self.last_card_label.config(text=text))

    def _update_round_multiplier(self, multiplier):
        """Update round multiplier display."""
        multiplier_text = f"Round: {multiplier}x"
        if multiplier > 1:
            multiplier_text += " (DOUBLED!)"
        self._safe_widget_operation(lambda: self.round_multiplier_label.config(text=multiplier_text))

    def _update_current_player(self, game_state):
        """Update current player indicator."""
        if self.widgets_destroyed:
            return
            
        if game_state.get("doubling_phase", False):
            current_idx = game_state.get("current_player_index", 0)
            players = game_state.get("players", [])
            if current_idx < len(players):
                player_name = players[current_idx]["name"]
                self._safe_widget_operation(lambda: self.turn_indicator_label.config(text=f"{player_name}'s Choice", fg="#ffeb3b"))
            return

        if game_state.get("round_active", False):
            current_idx = game_state.get("current_player_index", 0)
            players = game_state.get("players", [])
            forced_draw = game_state.get("forced_draw_in_progress", False)
            
            if current_idx < len(players):
                if self.game_mode == 'human_vs_human':
                    # In human vs human, show player names
                    player_name = players[current_idx]["name"]
                    if forced_draw:
                        self._safe_widget_operation(lambda: self.turn_indicator_label.config(text=f"{player_name}: Play Drawn Card", fg="#ff6600"))
                    else:
                        self._safe_widget_operation(lambda: self.turn_indicator_label.config(text=f"{player_name}'s Turn", fg="#90ee90"))
                else:
                    # In human vs AI, show Your Turn / Opponent's Turn
                    if current_idx == 0:
                        if forced_draw:
                            self._safe_widget_operation(lambda: self.turn_indicator_label.config(text="Play Drawn Card", fg="#ff6600"))
                        else:
                            self._safe_widget_operation(lambda: self.turn_indicator_label.config(text="Your Turn", fg="#90ee90"))
                    else:
                        self._safe_widget_operation(lambda: self.turn_indicator_label.config(text="Opponent's Turn", fg="#ffaa00"))
            else:
                self._safe_widget_operation(lambda: self.turn_indicator_label.config(text="Waiting...", fg="#cccccc"))
        else:
            self._safe_widget_operation(lambda: self.turn_indicator_label.config(text="Round Not Active", fg="#cccccc"))

    def _update_deck_size(self, deck_size):
        """Update deck size display."""
        self._safe_widget_operation(lambda: self.deck_size_label.config(text=f"Deck: {deck_size} cards"))

    def _update_player_info(self, players):
        """Update player information displays."""
        if len(players) >= 2:
            # Player 1 (bottom)
            player1 = players[0]
            self._safe_widget_operation(lambda: self.player_name_label.config(text=player1["name"]))
            self._safe_widget_operation(lambda: self.player_score_label.config(text=f"Score: {player1['score']}"))
            
            # Player 2 (top)
            player2 = players[1]
            self._safe_widget_operation(lambda: self.opponent_name_label.config(text=player2["name"]))
            self._safe_widget_operation(lambda: self.opponent_score_label.config(text=f"Score: {player2['score']}"))

    def _update_game_status(self, game_state):
        """Update game status display for special phases."""
        if self.widgets_destroyed:
            return
            
        if game_state.get("doubling_phase", False):
            current_idx = game_state.get("current_player_index", 0)
            players = game_state.get("players", [])
            multiplier = game_state.get("round_multiplier", 1)
            
            if current_idx < len(players):
                player_name = players[current_idx]["name"]
                
                if multiplier == 1:
                    text = f"{player_name}: Double the stakes?"
                else:
                    text = f"{player_name}: Redouble to 4x stakes?"
                self._safe_widget_operation(lambda: self.game_status_label.config(text=text))
        elif game_state.get("forced_draw_in_progress", False):
            self._safe_widget_operation(lambda: self.game_status_label.config(text="Drawn card must be played immediately!"))
        else:
            self._safe_widget_operation(lambda: self.game_status_label.config(text=""))

    def _update_player_hands(self):
        """Update player hand displays with enhanced card widgets."""
        if self.widgets_destroyed:
            return
            
        try:
            # Clear existing card widgets
            for widget in self.player_hand_frame.winfo_children():
                widget.destroy()
            for widget in self.opponent_hand_frame.winfo_children():
                widget.destroy()

            # Get players
            player1 = self.game_manager.get_player(0)
            player2 = self.game_manager.get_player(1)

            if player1:
                self._create_hand_display(player1, self.player_hand_frame, 0, face_up=True)
            
            if player2:
                # Show face up only in human vs human mode
                face_up = (self.game_mode == "human_vs_human")
                self._create_hand_display(player2, self.opponent_hand_frame, 1, face_up=face_up)
        except Exception as e:
            print(f"Error updating player hands: {e}")

    def _create_hand_display(self, player, parent_frame, player_index, face_up=True):
        """Create enhanced card display for a player's hand."""
        if self.widgets_destroyed:
            return
            
        try:
            hand = player.get_hand_copy()
            
            if not hand:
                # Create a "No Cards" label
                no_cards_label = tk.Label(
                    parent_frame,
                    text="No Cards",
                    font=('Arial', 14),
                    fg='#ffffff',
                    bg=parent_frame['bg']
                )
                no_cards_label.pack(expand=True)
                return
            
            # Create container for centering cards
            cards_container = tk.Frame(parent_frame, bg=parent_frame['bg'])
            cards_container.pack(expand=True)
            
            for i, card in enumerate(hand):
                try:
                    # FIXED: Make both players' cards clickable in human vs human mode
                    if self.game_mode == 'human_vs_human':
                        clickable = face_up  # Both players' cards are clickable
                    else:
                        clickable = (face_up and player_index == 0)  # Only human player in human vs AI
                    
                    card_widget = CardWidget(
                        cards_container,
                        card,
                        face_up=face_up,
                        clickable=clickable,
                        click_callback=lambda idx=i, pidx=player_index: self.on_card_clicked(pidx, idx)
                    )
                    card_widget.pack(side="left", padx=5, pady=10)
                    
                except Exception as e:
                    print(f"Error creating card widget for {card}: {e}")
                    # Create a simple placeholder if card widget fails
                    placeholder = tk.Label(
                        cards_container,
                        text=str(card),
                        font=('Arial', 10),
                        fg='#ffffff',
                        bg='#333333',
                        width=10,
                        height=5,
                        relief='raised',
                        bd=2
                    )
                    placeholder.pack(side="left", padx=3, pady=5)
            
        except Exception as e:
            print(f"Error in _create_hand_display: {e}")
            # Create error label
            error_label = tk.Label(
                parent_frame,
                text="Error displaying cards",
                font=('Arial', 12),
                fg='#ff0000',
                bg=parent_frame['bg']
            )
            error_label.pack(expand=True)

    def _update_button_states(self, game_state):
        """Update button states based on game state."""
        if self.widgets_destroyed:
            return
            
        current_player_index = game_state.get("current_player_index", 0)
        round_active = game_state.get("round_active", False)
        doubling_phase = game_state.get("doubling_phase", False)
        forced_draw = game_state.get("forced_draw_in_progress", False)
        
        # Get current player to check if they're human
        current_player = self.game_manager.get_player(current_player_index)
        is_current_player_human = current_player and current_player.is_human
        
        # FIXED: Doubling buttons - enable for ANY human player during doubling phase
        if doubling_phase and is_current_player_human:
            self._safe_widget_operation(lambda: self.double_button.config(state="normal", bg="#ff8c42"))
            self._safe_widget_operation(lambda: self.skip_doubling_button.config(state="normal", bg="#6c757d"))
        else:
            self._safe_widget_operation(lambda: self.double_button.config(state="disabled", bg="#6c757d"))
            self._safe_widget_operation(lambda: self.skip_doubling_button.config(state="disabled", bg="#6c757d"))
        
        # FIXED: Play card button - enable for current player in human vs human
        if self.game_mode == 'human_vs_human':
            can_play = (round_active and not doubling_phase and 
                       (self.selected_card is not None or forced_draw))
        else:
            can_play = (round_active and not doubling_phase and current_player_index == 0 and 
                       (self.selected_card is not None or forced_draw))
        
        self._safe_widget_operation(lambda: self.play_card_button.config(
            state="normal" if can_play else "disabled",
            bg="#4a90e2" if can_play else "#6c757d"
        ))
        
        # Draw card button (shown when player has no playable cards)
        player = self.game_manager.get_player(current_player_index) if self.game_mode == 'human_vs_human' else self.game_manager.get_player(0)
        show_draw = (round_active and not doubling_phase and 
                    ((self.game_mode == 'human_vs_human' and is_current_player_human) or 
                     (self.game_mode != 'human_vs_human' and current_player_index == 0)) and
                    player and not player.has_playable_cards(game_state["current_count"], game_state["last_card"]) and
                    not forced_draw)
        
        self._safe_widget_operation(lambda: self.draw_card_button.config(
            state="normal" if show_draw else "disabled",
            bg="#dc3545" if show_draw else "#6c757d"
        ))
        
        # Handle AI turn automatically (including doubling phase)
        if (current_player_index == 1 and self.game_mode == "human_vs_computer" and 
            not self.animation_active and not self.widgets_destroyed):
            
            if doubling_phase:
                # Handle AI doubling decision
                if hasattr(self, 'frame') and self.frame.winfo_exists():
                    self.frame.after(1500, self.handle_ai_doubling)
            elif round_active:
                # Handle regular AI turn
                if hasattr(self, 'frame') and self.frame.winfo_exists():
                    self.frame.after(1500, self.handle_ai_turn)

    def handle_double(self):
        """Handle doubling decision."""
        current_player_index = self.game_manager.current_player_index
        success = self.game_manager.handle_doubling(current_player_index, True)
        if success:
            self.selected_card = None

    def skip_doubling(self):
        """Skip the doubling phase."""
        self.game_manager.skip_doubling()
        self.selected_card = None

    def draw_stock_card(self):
        """Draw a card from the stock pile."""
        current_player_index = self.game_manager.current_player_index
        success = self.game_manager.draw_stock_card(current_player_index)
        if success:
            self.selected_card = None

    def handle_ai_doubling(self):
        """Handle AI doubling decision automatically"""
        if self.animation_active or self.widgets_destroyed:
            return
        
        current_player = self.game_manager.get_current_player()
        if not current_player or current_player.is_human:
            return
        
        game_state = self.game_manager.get_game_state()
        
        if game_state.get("doubling_phase", False):
            # Show AI thinking
            self._safe_widget_operation(lambda: self.turn_indicator_label.config(text="AI considering doubling...", fg="#ffaa00"))
            
            # Get AI doubling decision
            ai_wants_double = current_player.should_double(
                self.game_manager.round_multiplier, 
                game_state
            )
            
            # Apply the decision after thinking time
            thinking_time = getattr(current_player, 'thinking_time', 1.5) * 1000
            if hasattr(self, 'frame') and self.frame.winfo_exists():
                self.frame.after(int(thinking_time), 
                                lambda: self.game_manager.handle_doubling(1, ai_wants_double))

    def handle_ai_turn(self):
        """Handle AI player's turn automatically."""
        if self.animation_active or self.widgets_destroyed:
            return  # Don't interrupt animations
            
        current_player = self.game_manager.get_current_player()
        if not current_player or current_player.is_human:
            return  # Not AI's turn
        
        game_state = self.game_manager.get_game_state()
        
        # Get AI move
        ai_move = self.game_manager.get_ai_move()
        if not ai_move:
            # AI cannot play - this should trigger drawing
            return
        
        # Show AI thinking animation
        self.show_ai_thinking()
        
        # Schedule the actual move after thinking time
        thinking_time = getattr(current_player, 'thinking_time', 1.5) * 1000  # Convert to milliseconds
        if hasattr(self, 'frame') and self.frame.winfo_exists():
            self.frame.after(int(thinking_time), lambda: self.execute_ai_move(ai_move))

    def show_ai_thinking(self):
        """Show visual indication that AI is thinking."""
        self._safe_widget_operation(lambda: self.turn_indicator_label.config(text="AI Thinking...", fg="#ffaa00"))
        
        # Add blinking effect
        def blink():
            if self.widgets_destroyed:
                return
                
            try:
                current_color = self.turn_indicator_label.cget("fg")
                new_color = "#ff6600" if current_color == "#ffaa00" else "#ffaa00"
                self.turn_indicator_label.config(fg=new_color)
                
                # Continue blinking if still AI's turn
                current_player = self.game_manager.get_current_player()
                if current_player and not current_player.is_human and hasattr(self, 'frame') and self.frame.winfo_exists():
                    self.frame.after(500, blink)
            except tk.TclError:
                # Widget destroyed
                self.widgets_destroyed = True
        
        blink()

    def execute_ai_move(self, ai_move):
        """Execute the AI's chosen move."""
        if not ai_move or self.widgets_destroyed:
            return
        
        try:
            # Extract move data
            card_index = ai_move['card_index']
            action_data = ai_move.get('action_data', {})
            
            # Play the card
            success = self.game_manager.play_card(1, card_index, action_data)  # Player index 1 = AI
            
            if success:
                # Show what AI played
                card = ai_move['card']
                self.show_ai_move_feedback(card, action_data)
            else:
                print(f"AI move failed: {ai_move}")
                
        except Exception as e:
            print(f"Error executing AI move: {e}")

    def show_ai_move_feedback(self, card, action_data):
        """Show feedback about what the AI played."""
        if self.widgets_destroyed:
            return
            
        try:
            # Create a temporary feedback label
            feedback_frame = tk.Frame(self.center_frame, bg='#5a8a69')
            feedback_frame.place(relx=0.5, rely=0.15, anchor='center')
            
            # Determine move description
            move_description = f"AI played {card}"
            
            if action_data:
                if 'value' in action_data:
                    if card.is_ace():
                        move_description += f" as {action_data['value']}"
                    elif card.rank == 'K':
                        move_description += f" ÷ {action_data['value']}"
            
            feedback_label = tk.Label(
                feedback_frame,
                text=move_description,
                font=('Arial', 12, 'bold'),
                fg='#ffffff',
                bg='#ff8c42',
                padx=20,
                pady=10,
                relief='raised',
                bd=2
            )
            feedback_label.pack()
            
            # Remove feedback after delay
            if hasattr(self, 'frame') and self.frame.winfo_exists():
                self.frame.after(2500, lambda: feedback_frame.destroy() if feedback_frame.winfo_exists() else None)
        except Exception as e:
            print(f"Error showing AI feedback: {e}")

    def _show_draw_notification(self, player_name, card):
        """Show notification when a player draws a card."""
        if self.widgets_destroyed:
            return
            
        try:
            # Create temporary notification
            notification_frame = tk.Frame(self.center_frame, bg='#5a8a69')
            notification_frame.place(relx=0.5, rely=0.85, anchor='center')
            
            notification_label = tk.Label(
                notification_frame,
                text=f"{player_name} drew a card from stock",
                font=('Arial', 13, 'bold'),
                fg='#ffffff',
                bg='#6c757d',
                padx=20,
                pady=10,
                relief='raised',
                bd=2
            )
            notification_label.pack()
            
            # Remove notification after delay
            if hasattr(self, 'frame') and self.frame.winfo_exists():
                self.frame.after(3000, lambda: notification_frame.destroy() if notification_frame.winfo_exists() else None)
        except Exception as e:
            print(f"Error showing draw notification: {e}")

    def on_card_clicked(self, player_index, card_index):
        """Handle card click events."""
        if self.widgets_destroyed:
            return
            
        # FIXED: Allow both players to select cards in human vs human mode
        current_player_index = self.game_manager.current_player_index
        
        if self.game_mode == 'human_vs_human':
            # In human vs human, only current player can select cards
            if player_index != current_player_index:
                return
        else:
            # In human vs AI, only player 1 can select cards
            if player_index != 0:
                return
        
        try:
            # Clear previous selection visually
            for widget in self.player_hand_frame.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for card_container in widget.winfo_children():
                        if hasattr(card_container, 'set_selected'):
                            card_container.set_selected(False)
            
            for widget in self.opponent_hand_frame.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for card_container in widget.winfo_children():
                        if hasattr(card_container, 'set_selected'):
                            card_container.set_selected(False)
            
            self.selected_card = (player_index, card_index)
            
            # Highlight selected card
            if player_index == 0:
                cards = list(self.player_hand_frame.winfo_children())[0].winfo_children()
            else:
                cards = list(self.opponent_hand_frame.winfo_children())[0].winfo_children()
                
            if card_index < len(cards):
                if hasattr(cards[card_index], 'set_selected'):
                    cards[card_index].set_selected(True)
            
            # Update button state
            game_state = self.game_manager.get_game_state()
            self._update_button_states(game_state)
        except Exception as e:
            print(f"Error handling card click: {e}")

    def play_selected_card(self):
        """Play the currently selected card."""
        if self.widgets_destroyed:
            return
            
        game_state = self.game_manager.get_game_state()
        
        # Handle forced draw scenario
        if game_state.get("forced_draw_in_progress", False):
            current_player_index = self.game_manager.current_player_index
            player = self.game_manager.get_player(current_player_index)
            
            if player and player.hand:
                # The drawn card should be the last one added
                last_card_index = len(player.hand) - 1
                last_card = player.hand[last_card_index]
                
                if player.can_play_card(last_card, self.game_manager.current_count, self.game_manager.last_card):
                    options = player.get_card_options(last_card, self.game_manager.current_count)
                    
                    action_data = None
                    if len(options) > 1:
                        # Show action selection dialog
                        dialog = ActionDialog(self.frame, last_card, options)
                        if dialog.result:
                            action_data = {
                                'action': dialog.result['action'],
                                'value': dialog.result.get('value')
                            }
                        else:
                            return  # User cancelled
                    
                    # Play the drawn card
                    success = self.game_manager.play_card(current_player_index, last_card_index, action_data)
                    if success:
                        self.selected_card = None
                    else:
                        messagebox.showerror("Invalid Move", "That card cannot be played right now.")
                else:
                    messagebox.showerror("Invalid Move", "The drawn card cannot be played.")
            return
        
        # Normal card play
        if not self.selected_card:
            messagebox.showwarning("No Card Selected", "Please select a card to play.")
            return

        player_index, card_index = self.selected_card
        player = self.game_manager.get_player(player_index)
        card = player.get_card_at_index(card_index)

        if not card:
            messagebox.showerror("Error", "Invalid card selection.")
            return

        # Check if card has multiple play options
        current_count = self.game_manager.current_count
        last_card = self.game_manager.last_card
        
        options = player.get_card_options(card, current_count)
        
        action_data = None
        if len(options) > 1:
            # Show action selection dialog
            dialog = ActionDialog(self.frame, card, options)
            if dialog.result:
                action_data = {
                    'action': dialog.result['action'],
                    'value': dialog.result.get('value')
                }
            else:
                return  # User cancelled

        # Play the card
        success = self.game_manager.play_card(player_index, card_index, action_data)
        
        if success:
            self.selected_card = None
        else:
            messagebox.showerror("Invalid Move", "That card cannot be played right now.")

    def _show_card_played_animation(self, player_index, card):
        """Show animation for card being played with error handling."""
        if self.widgets_destroyed:
            return
            
        try:
            # Enhanced visual feedback with safe operations
            original_bg = self._safe_widget_operation(lambda: self.count_label.cget("bg"))
            if original_bg is not None:
                self._safe_widget_operation(lambda: self.count_label.config(bg="#ffff88"))
                if hasattr(self, 'frame') and self.frame.winfo_exists():
                    self.frame.after(400, lambda: self._safe_widget_operation(lambda: self.count_label.config(bg=original_bg)))
        except Exception as e:
            print(f"Error in card animation: {e}")

    def start_new_round(self):
        """Start a new round."""
        if self.game_manager.start_new_round():
            self._safe_widget_operation(lambda: self.new_round_button.config(state="disabled"))
            self.selected_card = None

    def start_new_game(self):
        """Start a completely new game."""
        self.game_manager.reset_game()
        self.game_manager.start_new_round()
        self._safe_widget_operation(lambda: self.new_round_button.config(state="disabled"))
        self.selected_card = None

    def return_to_menu(self):
        """Return to the main menu."""
        if messagebox.askyesno("Return to Menu", "Are you sure you want to return to the main menu?"):
            self.main_window.show_menu_screen()

    def destroy(self):
        """Clean up the game screen."""
        self.widgets_destroyed = True
        if hasattr(self, 'frame'):
            try:
                self.frame.destroy()
            except tk.TclError:
                pass  # Already destroyed