"""
Rules screen for Limbo Card Game GUI - Updated with complete rules
"""

import tkinter as tk
from tkinter import ttk

class RulesScreen:
    """Screen displaying complete game rules and how to play"""
    
    def __init__(self, parent, main_window):
        """Initialize rules screen"""
        self.parent = parent
        self.main_window = main_window
        self.create_screen()
    
    def create_screen(self):
        """Create the rules screen layout"""
        # Main frame
        self.frame = tk.Frame(self.parent, bg='#f0f0f0')
        self.frame.pack(fill='both', expand=True)
        
        # Create header
        self.create_header()
        
        # Create tabbed content
        self.create_tabbed_content()
        
        # Create footer with navigation
        self.create_footer()
    
    def create_header(self):
        """Create screen header"""
        header_frame = tk.Frame(self.frame, bg='#1a1a2e', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="LIMBO CARD GAME - COMPLETE RULES v2.0",
            font=('Arial', 24, 'bold'),
            fg='#ffffff',
            bg='#1a1a2e'
        )
        title_label.pack(expand=True)
    
    def create_tabbed_content(self):
        """Create tabbed content area"""
        content_frame = tk.Frame(self.frame, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_overview_tab()
        self.create_cards_tab()
        self.create_gameplay_tab()
        self.create_drawing_tab()  # NEW TAB
        self.create_doubling_tab()  # NEW TAB
        self.create_scoring_tab()
        self.create_strategy_tab()
    
    def create_overview_tab(self):
        """Create overview tab"""
        overview_frame = tk.Frame(self.notebook, bg='white', padx=20, pady=20)
        self.notebook.add(overview_frame, text="📖 Overview")
        
        # Create scrollable text
        canvas = tk.Canvas(overview_frame, bg='white')
        scrollbar = ttk.Scrollbar(overview_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Overview content
        self.add_overview_content(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_overview_content(self, parent):
        """Add overview content"""
        content = [
            ("What is Limbo?", 
             "Limbo is a strategic card game for two players where the goal is to reduce a count from 101 to zero without going below zero. The last player able to make a legal move wins the round!"),
            
            ("Game Objective",
             "Be the last player able to play a card without making the count go below zero. Each round, the winner scores points, and the first player to reach the target score wins the game."),
            
            ("What You Need",
             "• A standard 52-card deck\n• Two players\n• This Limbo game application"),
            
            ("Quick Start",
             "1. Each player gets 5 cards\n2. Optional doubling phase\n3. Start with count of 101\n4. Take turns playing cards to reduce the count\n5. Can't play? Draw from stock pile!\n6. Don't let the count go below zero!\n7. Last player to play wins the round"),
            
            ("🆕 NEW IN VERSION 2.0",
             "✅ Complete card drawing mechanics\n✅ Proper doubling/redoubling phase\n✅ Forced play of drawable cards\n✅ Enhanced AI strategic thinking\n✅ Better visual feedback and indicators\n✅ 100% rule compliance with David Parlett's original"),
            
            ("Game Flow",
             "The game consists of multiple rounds. Each round:\n• Players are dealt 5 cards\n• Optional doubling phase (non-dealer first, then dealer)\n• Dealer plays starting card from stock\n• Players alternate playing cards\n• If no playable cards: draw from stock\n• If drawn card is playable: must play immediately\n• Round ends when someone can't play or stock is empty\n• Winner scores points\n• Continue until target score reached")
        ]
        
        for title, text in content:
            # Section title
            title_label = tk.Label(
                parent,
                text=title,
                font=('Arial', 16, 'bold'),
                fg='#1a1a2e',
                bg='white'
            )
            title_label.pack(anchor='w', pady=(20, 10))
            
            # Section content
            content_label = tk.Label(
                parent,
                text=text,
                font=('Arial', 12),
                fg='#333',
                bg='white',
                justify='left',
                wraplength=700
            )
            content_label.pack(anchor='w', pady=(0, 10))
    
    def create_cards_tab(self):
        """Create cards reference tab"""
        cards_frame = tk.Frame(self.notebook, bg='white', padx=20, pady=20)
        self.notebook.add(cards_frame, text="🃏 Cards")
        
        # Create scrollable content
        canvas = tk.Canvas(cards_frame, bg='white')
        scrollbar = ttk.Scrollbar(cards_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Cards content
        self.add_cards_content(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_cards_content(self, parent):
        """Add cards reference content"""
        tk.Label(
            parent,
            text="CARD TYPES AND EFFECTS",
            font=('Arial', 18, 'bold'),
            fg='#1a1a2e',
            bg='white'
        ).pack(pady=(0, 20))
        
        card_types = [
            ("NUMBER CARDS (2-10)", "#0066cc", [
                "• Can SUBTRACT the card value from count",
                "• Can DIVIDE the count by card value (if it divides evenly)",
                "• ⚠️ DIVISION IS MANDATORY when possible",
                "• Example: Count is 96, play 6 → MUST divide (96÷6=16)",
                "• Example: Count is 95, play 6 → subtract (95-6=89)"
            ]),
            
            ("ACES (A)", "#cc0000", [
                "• Can be played as 1 OR 11 (your choice)",
                "• Always SUBTRACTS - cannot divide",
                "• Very flexible for fine-tuning the count",
                "• Example: Count is 12, Ace as 1 → 11, Ace as 11 → 1",
                "• Great for precise endgame positioning"
            ]),
            
            ("JACK (J)", "#009900", [
                "• Repeats the effect of the PREVIOUS card played",
                "• If last card was a 7, Jack acts like a 7",
                "• If last card was a Queen, Jack reverses digits",
                "• Cannot be played if no previous card",
                "• Very situational but potentially powerful"
            ]),
            
            ("QUEEN (Q)", "#cc6600", [
                "• REVERSES the digits of the current count",
                "• Only playable if reversing REDUCES the count",
                "• Example: 91 → 19 (good), but 19 → 91 (not allowed)",
                "• Example: 60 → 06 = 6 (very powerful!)",
                "• Great for counts ending in 1, 2, 3, etc."
            ]),
            
            ("KING (K)", "#6600cc", [
                "• DIVIDES count by ANY number you choose",
                "• Divisor must be > 1 and < current count",
                "• Division must result in NO REMAINDER",
                "• Most powerful card - can create huge reductions",
                "• Example: Count 60, divide by 15 → 4",
                "• Choose divisor strategically!"
            ])
        ]
        
        for title, color, effects in card_types:
            # Card type header
            header_frame = tk.Frame(parent, bg=color, height=40)
            header_frame.pack(fill='x', pady=(10, 0))
            header_frame.pack_propagate(False)
            
            tk.Label(
                header_frame,
                text=title,
                font=('Arial', 14, 'bold'),
                fg='white',
                bg=color
            ).pack(expand=True)
            
            # Effects list
            effects_frame = tk.Frame(parent, bg='#f8f8f8', relief='solid', bd=1)
            effects_frame.pack(fill='x', pady=(0, 10))
            
            for effect in effects:
                tk.Label(
                    effects_frame,
                    text=effect,
                    font=('Arial', 11),
                    fg='#333',
                    bg='#f8f8f8',
                    anchor='w'
                ).pack(fill='x', padx=10, pady=2)
    
    def create_gameplay_tab(self):
        """Create gameplay tab"""
        gameplay_frame = tk.Frame(self.notebook, bg='white', padx=20, pady=20)
        self.notebook.add(gameplay_frame, text="🎮 Gameplay")
        
        # Create scrollable content
        canvas = tk.Canvas(gameplay_frame, bg='white')
        scrollbar = ttk.Scrollbar(gameplay_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Gameplay content
        self.add_gameplay_content(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_gameplay_content(self, parent):
        """Add gameplay content"""
        sections = [
            ("ROUND SETUP", [
                "1. Shuffle deck and deal 5 cards to each player",
                "2. Remaining cards form face-down stock pile",
                "3. Set count to 101",
                "4. Decide who goes first (non-dealer)"
            ]),
            
            ("STARTING CARD", [
                "• Dealer plays top card from stock pile",
                "• If it's a face card (J,Q,K), count stays 101",
                "• If it's a number card, subtract from 101",
                "• If it's an Ace, subtract 1 from 101",
                "• This counts as the first card played"
            ]),
            
            ("PLAYER TURNS", [
                "1. Current player must play a card from hand",
                "2. Card effect is applied to the count",
                "3. Count cannot go below zero",
                "4. If player cannot play, they must draw from stock",
                "5. Turn passes to other player"
            ]),
            
            ("ROUND END CONDITIONS", [
                "• Player reduces count to exactly zero",
                "• Player runs out of cards (and can't continue with stock)",
                "• Player cannot play and stock is empty",
                "• The player who made the last legal move wins"
            ])
        ]
        
        for title, items in sections:
            # Section title
            title_label = tk.Label(
                parent,
                text=title,
                font=('Arial', 16, 'bold'),
                fg='#1a1a2e',
                bg='white'
            )
            title_label.pack(anchor='w', pady=(20, 10))
            
            # Section items
            for item in items:
                item_label = tk.Label(
                    parent,
                    text=item,
                    font=('Arial', 12),
                    fg='#333',
                    bg='white',
                    justify='left',
                    wraplength=700
                )
                item_label.pack(anchor='w', pady=2, padx=20)
    
    def create_drawing_tab(self):
        """Create card drawing rules tab"""
        drawing_frame = tk.Frame(self.notebook, bg='white', padx=20, pady=20)
        self.notebook.add(drawing_frame, text="🎲 Drawing Cards")
        
        # Create scrollable content
        canvas = tk.Canvas(drawing_frame, bg='white')
        scrollbar = ttk.Scrollbar(drawing_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Drawing content
        self.add_drawing_content(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_drawing_content(self, parent):
        """Add card drawing rules content"""
        tk.Label(
            parent,
            text="CARD DRAWING MECHANICS",
            font=('Arial', 18, 'bold'),
            fg='#1a1a2e',
            bg='white'
        ).pack(pady=(0, 20))
        
        sections = [
            ("🎯 WHEN CAN YOU DRAW?", "#dc3545", [
                "• Only when it's your turn",
                "• Only if you have NO playable cards in hand",
                "• Only if the stock pile is not empty",
                "• You CANNOT voluntarily draw if you have playable cards"
            ]),
            
            ("📤 HOW DOES DRAWING WORK?", "#28a745", [
                "1. Draw the top card from the stock pile",
                "2. Check if the drawn card is playable",
                "3. If playable: MUST play it immediately",
                "4. If not playable: keep it and end your turn",
                "5. Turn passes to opponent"
            ]),
            
            ("⚡ FORCED PLAY RULE", "#ff8c42", [
                "• If you draw a playable card, you MUST play it",
                "• No choice - immediate play is mandatory",
                "• For Aces/Kings: game chooses best option automatically",
                "• Your hand size stays the same (draw + play = net zero)"
            ]),
            
            ("❌ WHEN DRAWING FAILS", "#6c757d", [
                "• If stock pile is empty and you can't play",
                "• You forfeit the round immediately",
                "• Opponent wins regardless of current count",
                "• This is why managing your hand is crucial"
            ]),
            
            ("💡 STRATEGIC IMPLICATIONS", "#6600cc", [
                "• Try to avoid situations where you can't play",
                "• Save flexible cards (Aces, face cards) for emergencies",
                "• Watch the stock pile size",
                "• Force opponents into drawing scenarios",
                "• Drawing can sometimes save you with a lucky card!"
            ])
        ]
        
        for title, color, items in sections:
            # Section header
            header_frame = tk.Frame(parent, bg=color, height=35)
            header_frame.pack(fill='x', pady=(15, 0))
            header_frame.pack_propagate(False)
            
            tk.Label(
                header_frame,
                text=title,
                font=('Arial', 14, 'bold'),
                fg='white',
                bg=color
            ).pack(expand=True)
            
            # Items list
            items_frame = tk.Frame(parent, bg='#f8f8f8', relief='solid', bd=1)
            items_frame.pack(fill='x', pady=(0, 5))
            
            for item in items:
                tk.Label(
                    items_frame,
                    text=item,
                    font=('Arial', 11),
                    fg='#333',
                    bg='#f8f8f8',
                    anchor='w',
                    wraplength=650
                ).pack(fill='x', padx=15, pady=3)
    
    def create_doubling_tab(self):
        """Create doubling phase tab"""
        doubling_frame = tk.Frame(self.notebook, bg='white', padx=20, pady=20)
        self.notebook.add(doubling_frame, text="💰 Doubling")
        
        content = [
            ("DOUBLING PHASE OVERVIEW", 
             "Before each round begins, players can choose to increase the stakes through doubling and redoubling. This affects the winner's final score for that round."),
            
            ("DOUBLING SEQUENCE",
             "1. NON-DEALER goes first and may choose to DOUBLE\n"
             "2. If doubled, DEALER may choose to REDOUBLE\n"
             "3. If no doubling, round starts at normal stakes (1x)\n"
             "4. If doubled but not redoubled, stakes are 2x\n"
             "5. If redoubled, stakes are 4x"),
            
            ("DOUBLING EFFECTS",
             "• WINNER gets: (normal score) × (multiplier)\n"
             "• LOSER gets: normal score (no multiplier applied)\n"
             "• Doubling only affects the winner's score\n"
             "• This creates strategic risk/reward decisions"),
            
            ("EXAMPLE SCORING",
             "Round ends with 8 cards played, final count 5:\n\n"
             "Normal (1x): Winner 80, Loser 50\n"
             "Doubled (2x): Winner 160, Loser 50\n"
             "Redoubled (4x): Winner 320, Loser 50\n\n"
             "The loser's score never changes!"),
            
            ("STRATEGIC CONSIDERATIONS",
             "• Double with strong hands (face cards, good Aces)\n"
             "• Don't double with weak hands (high numbers only)\n"
             "• Consider your opponent's likely hand strength\n"
             "• Redoubling is very risky - only with excellent hands\n"
             "• Use doubling to catch up when behind in score")
        ]
        
        for title, text in content:
            # Section title
            title_label = tk.Label(
                doubling_frame,
                text=title,
                font=('Arial', 16, 'bold'),
                fg='#1a1a2e',
                bg='white'
            )
            title_label.pack(anchor='w', pady=(20, 10))
            
            # Section content
            content_label = tk.Label(
                doubling_frame,
                text=text,
                font=('Arial', 12),
                fg='#333',
                bg='white',
                justify='left',
                wraplength=700
            )
            content_label.pack(anchor='w', pady=(0, 10))
    
    def create_scoring_tab(self):
        """Create scoring tab"""
        scoring_frame = tk.Frame(self.notebook, bg='white', padx=20, pady=20)
        self.notebook.add(scoring_frame, text="🏆 Scoring")
        
        content = [
            ("ROUND SCORING", 
             "At the end of each round:\n\n"
             "WINNER gets: 10 × (number of cards played in round) × (doubling multiplier)\n"
             "LOSER gets: 10 × (final count value)\n\n"
             "Note: Doubling multiplier ONLY applies to winner's score!\n\n"
             "Example: 8 cards played, final count 3, game was doubled\n"
             "Winner: 10 × 8 × 2 = 160 points\n"
             "Loser: 10 × 3 = 30 points"),
            
            ("GAME SCORING",
             "• Default target score: 200 points\n"
             "• First player to reach target wins the game\n"
             "• Target can be customized when starting game\n"
             "• Recommended ranges: 100-500 points"),
            
            ("STRATEGIC IMPLICATIONS",
             "• Winners benefit from longer rounds (more cards played)\n"
             "• Losers benefit from higher final counts\n"
             "• Doubling is risky but can lead to big point swings\n"
             "• Consider your hand strength before doubling\n"
             "• Sometimes it's better to lose quickly than slowly!")
        ]
        
        for title, text in content:
            # Section title
            title_label = tk.Label(
                scoring_frame,
                text=title,
                font=('Arial', 16, 'bold'),
                fg='#1a1a2e',
                bg='white'
            )
            title_label.pack(anchor='w', pady=(20, 10))
            
            # Section content
            content_label = tk.Label(
                scoring_frame,
                text=text,
                font=('Arial', 12),
                fg='#333',
                bg='white',
                justify='left',
                wraplength=700
            )
            content_label.pack(anchor='w', pady=(0, 10))
    
    def create_strategy_tab(self):
        """Create strategy tips tab"""
        strategy_frame = tk.Frame(self.notebook, bg='white', padx=20, pady=20)
        self.notebook.add(strategy_frame, text="🧠 Strategy")
        
        # Create scrollable content
        canvas = tk.Canvas(strategy_frame, bg='white')
        scrollbar = ttk.Scrollbar(strategy_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Strategy content
        self.add_strategy_content(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_strategy_content(self, parent):
        """Add strategy content"""
        strategies = [
            ("BASIC STRATEGY", [
                "• Division is usually better than subtraction",
                "• Try to leave difficult numbers for your opponent",
                "• Prime numbers (2, 3, 5, 7, 11, 13...) are often good targets",
                "• Avoid leaving easy multiples (4, 6, 8, 9, 10, 12, 15, 16, 18, 20)"
            ]),
            
            ("CARD MANAGEMENT", [
                "• Save flexible cards (Aces, Kings, Queens) for emergencies",
                "• Use number cards early when division is available",
                "• Don't waste Jacks - wait for good previous cards",
                "• Keep track of what cards have been played"
            ]),
            
            ("DRAWING STRATEGY", [
                "• Avoid situations where you might be forced to draw",
                "• When you must draw, hope for Aces or face cards",
                "• Force opponents into drawing scenarios when possible",
                "• Watch the stock pile size carefully",
                "• Sometimes drawing can save you with the right card!"
            ]),
            
            ("ENDGAME TACTICS", [
                "• When count is below 20, be extra careful",
                "• Try to force opponent into single digits",
                "• Count of 1 is often game-ending (opponent needs Ace)",
                "• Counts 2, 3, 5, 7 are difficult to escape",
                "• Avoid giving opponent counts like 4, 6, 8, 9"
            ]),
            
            ("DOUBLING DECISIONS", [
                "• Double with strong hands (multiple face cards)",
                "• Don't double with weak hands (mostly high numbers)",
                "• Consider game score - double when behind",
                "• Redoubling is very risky - only with excellent hands",
                "• Watch opponent's reactions to gauge their hand strength"
            ]),
            
            ("PSYCHOLOGICAL TACTICS", [
                "• Vary your play style to be unpredictable",
                "• Sometimes make suboptimal moves to confuse",
                "• Pay attention to what cards have been played",
                "• Watch timing - quick plays vs. long thinks",
                "• Use doubling as psychological pressure"
            ]),
            
            ("COMMON MISTAKES", [
                "• Forgetting that division is mandatory",
                "• Playing face cards too early in the round",
                "• Not considering opponent's possible responses",
                "• Doubling with weak hands",
                "• Focusing only on immediate reduction, not strategy",
                "• Not managing cards to avoid forced drawing"
            ])
        ]
        
        for title, tips in strategies:
            # Strategy section header
            header_frame = tk.Frame(parent, bg='#4CAF50', height=35)
            header_frame.pack(fill='x', pady=(15, 0))
            header_frame.pack_propagate(False)
            
            tk.Label(
                header_frame,
                text=title,
                font=('Arial', 14, 'bold'),
                fg='white',
                bg='#4CAF50'
            ).pack(expand=True)
            
            # Tips list
            tips_frame = tk.Frame(parent, bg='#f1f8e9', relief='solid', bd=1)
            tips_frame.pack(fill='x', pady=(0, 5))
            
            for tip in tips:
                tk.Label(
                    tips_frame,
                    text=tip,
                    font=('Arial', 11),
                    fg='#333',
                    bg='#f1f8e9',
                    anchor='w',
                    wraplength=650
                ).pack(fill='x', padx=15, pady=3)
    
    def create_footer(self):
        """Create footer with navigation"""
        footer_frame = tk.Frame(self.frame, bg='#2a2a2a', height=80)
        footer_frame.pack(fill='x')
        footer_frame.pack_propagate(False)
        
        # Navigation buttons with better styling
        button_frame = tk.Frame(footer_frame, bg='#2a2a2a')
        button_frame.pack(expand=True)
        
        # Custom button style for better visibility
        button_style = {
            'font': ('Arial', 12, 'bold'),
            'fg': 'white',
            'bg': '#4a6741',
            'activebackground': '#5a7751',
            'activeforeground': 'white',
            'relief': 'raised',
            'bd': 2,
            'padx': 20,
            'pady': 10
        }
        
        main_menu_btn = tk.Button(
            button_frame,
            text="🏠 Main Menu",
            command=self.return_to_menu,
            **button_style
        )
        main_menu_btn.pack(side='left', padx=20, pady=15)
        
        start_game_btn = tk.Button(
            button_frame,
            text="🎮 Start Game",
            command=self.start_game,
            **button_style
        )
        start_game_btn.pack(side='left', padx=20, pady=15)
        
        settings_btn = tk.Button(
            button_frame,
            text="⚙️ Settings",
            command=self.show_settings,
            **button_style
        )
        settings_btn.pack(side='left', padx=20, pady=15)
    
    def return_to_menu(self):
        """Return to main menu"""
        self.main_window.show_menu_screen()
    
    def start_game(self):
        """Start a new game"""
        self.main_window.show_game_screen()
    
    def show_settings(self):
        """Show settings screen"""
        self.main_window.show_settings_screen()
    
    def destroy(self):
        """Destroy the rules screen"""
        if hasattr(self, 'frame') and self.frame:
            self.frame.destroy()