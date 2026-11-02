"""
Card class for Limbo GUI game
"""

class Card:
    """Represents a playing card with suit and rank"""
    
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    # Suit symbols for display
    SUIT_SYMBOLS = {
        'Hearts': '♥',
        'Diamonds': '♦',
        'Clubs': '♣',
        'Spades': '♠'
    }
    
    # Suit colors for GUI display
    SUIT_COLORS = {
        'Hearts': '#DC143C',      # Crimson
        'Diamonds': '#FF6347',    # Tomato
        'Clubs': '#000000',       # Black
        'Spades': '#000000'       # Black
    }
    
    def __init__(self, suit, rank):
        """Initialize a card with suit and rank"""
        if suit not in self.SUITS:
            raise ValueError(f"Invalid suit: {suit}")
        if rank not in self.RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        """String representation of the card"""
        return f"{self.rank} of {self.suit}"
    
    def __repr__(self):
        """Object representation of the card"""
        return f"Card('{self.suit}', '{self.rank}')"
    
    def __eq__(self, other):
        """Check if two cards are equal"""
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank
    
    def __hash__(self):
        """Make card hashable for use in sets/dicts"""
        return hash((self.suit, self.rank))
    
    def get_value(self):
        """Get the numeric value of the card for calculations"""
        if self.rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            return int(self.rank)
        elif self.rank == 'A':
            return 1  # Can be 1 or 11, but default to 1
        else:  # J, Q, K
            return 0  # Face cards have special rules
    
    def is_face_card(self):
        """Check if this is a face card (J, Q, K)"""
        return self.rank in ['J', 'Q', 'K']
    
    def is_ace(self):
        """Check if this is an Ace"""
        return self.rank == 'A'
    
    def is_number_card(self):
        """Check if this is a number card (2-10)"""
        return self.rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10']
    
    def get_short_name(self):
        """Get a short representation of the card for display"""
        return f"{self.rank}{self.SUIT_SYMBOLS.get(self.suit, self.suit[0])}"
    
    def get_display_name(self):
        """Get display name with suit symbol"""
        return f"{self.rank}{self.SUIT_SYMBOLS[self.suit]}"
    
    def get_suit_symbol(self):
        """Get the suit symbol"""
        return self.SUIT_SYMBOLS[self.suit]
    
    def get_suit_color(self):
        """Get the color for this card's suit"""
        return self.SUIT_COLORS[self.suit]
    
    def is_red_suit(self):
        """Check if this card has a red suit"""
        return self.suit in ['Hearts', 'Diamonds']
    
    def is_black_suit(self):
        """Check if this card has a black suit"""
        return self.suit in ['Clubs', 'Spades']
    
    def get_card_image_name(self):
        """Get the image filename for this card (for future image support)"""
        suit_abbrev = {
            'Hearts': 'H',
            'Diamonds': 'D',
            'Clubs': 'C',
            'Spades': 'S'
        }
        return f"{self.rank}_{suit_abbrev[self.suit]}.png"
    
    def get_description(self):
        """Get a full description of the card and its game effect"""
        descriptions = {
            'A': f"Ace of {self.suit} - Can be played as 1 or 11 (subtract only)",
            'J': f"Jack of {self.suit} - Repeats the effect of the previous card",
            'Q': f"Queen of {self.suit} - Reverses the digits of the current count",
            'K': f"King of {self.suit} - Divides by any chosen valid divisor"
        }
        
        if self.rank in descriptions:
            return descriptions[self.rank]
        else:
            return f"{self.rank} of {self.suit} - Subtract {self.get_value()} or divide by {self.get_value()} if possible"