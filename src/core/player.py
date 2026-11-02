"""
Player class for Limbo GUI game
Updated with correct Limbo rules
"""

from .card import Card

class Player:
    """Represents a player in the Limbo game"""
    
    def __init__(self, name, is_human=True):
        """Initialize a player with a name and type"""
        self.name = name
        self.is_human = is_human
        self.hand = []
        self.score = 0
        self.rounds_won = 0
        self.cards_played_this_round = 0
        self.total_cards_played = 0
        self.is_active = True  # Whether player can currently play
    
    def add_card(self, card):
        """Add a card to the player's hand"""
        if isinstance(card, Card):
            self.hand.append(card)
        else:
            raise ValueError("Only Card objects can be added to hand")
    
    def add_multiple_cards(self, cards):
        """Add multiple cards to the player's hand"""
        for card in cards:
            self.add_card(card)
    
    def play_card(self, card_index):
        """Play a card from the hand at the given index"""
        if 0 <= card_index < len(self.hand):
            card = self.hand.pop(card_index)
            self.cards_played_this_round += 1
            self.total_cards_played += 1
            return card
        else:
            raise IndexError("Invalid card index")
    
    def play_card_by_reference(self, card):
        """Play a specific card from the hand"""
        if card in self.hand:
            index = self.hand.index(card)
            return self.play_card(index)
        else:
            raise ValueError("Card not in player's hand")
    
    def get_hand_size(self):
        """Get the number of cards in hand"""
        return len(self.hand)
    
    def has_cards(self):
        """Check if player has any cards"""
        return len(self.hand) > 0
    
    def get_card_at_index(self, index):
        """Get card at specific index without removing it"""
        if 0 <= index < len(self.hand):
            return self.hand[index]
        return None
    
    def get_hand_copy(self):
        """Get a copy of the player's hand"""
        return self.hand.copy()
    
    def clear_hand(self):
        """Remove all cards from hand"""
        self.hand.clear()
    
    def add_score(self, points):
        """Add points to player's score"""
        self.score += points
    
    def add_round_win(self):
        """Increment rounds won counter"""
        self.rounds_won += 1
    
    def reset_score(self):
        """Reset player's score to 0"""
        self.score = 0
        self.rounds_won = 0
    
    def reset_round_stats(self):
        """Reset round-specific statistics"""
        self.cards_played_this_round = 0
        self.is_active = True
    
    def set_inactive(self):
        """Set player as inactive (cannot play)"""
        self.is_active = False
    
    def set_active(self):
        """Set player as active (can play)"""
        self.is_active = True
    
    def get_playable_cards(self, current_count, last_card=None):
        """Get list of cards that can be played given current game state"""
        playable = []
        
        for i, card in enumerate(self.hand):
            if self.can_play_card(card, current_count, last_card):
                playable.append((i, card))
        
        return playable
    
    def can_play_card(self, card, current_count, last_card=None):
        """Check if a specific card can be played without going below zero"""
        if current_count <= 0:
            return False
        
        if card.is_number_card():
            value = card.get_value()
            # Check division first (mandatory if possible)
            if current_count % value == 0:
                # Can divide - this is the only option
                result = current_count // value
                return result >= 0
            else:
                # Can only subtract if division is not possible
                result = current_count - value
                return result >= 0
        
        elif card.is_ace():
            # Ace can be 1 or 11, check both possibilities
            return (current_count - 1 >= 0) or (current_count - 11 >= 0)
        
        elif card.rank == 'J':
            # Jack repeats last card effect - need previous card
            if not last_card:
                return False
            # Simulate the last card's effect
            return self._can_repeat_card_effect(last_card, current_count)
        
        elif card.rank == 'Q':
            # Queen reverses digits only if it reduces count
            try:
                if current_count < 10:
                    return False  # Can't meaningfully reverse single digit
                reversed_count = int(str(current_count)[::-1])
                return reversed_count < current_count and reversed_count >= 0
            except ValueError:
                return False
        
        elif card.rank == 'K':
            # King can divide by any valid divisor
            for divisor in range(2, current_count):
                if current_count % divisor == 0:
                    return True
            return False
        
        return False
    
    def _can_repeat_card_effect(self, last_card, current_count):
        """Check if jack can repeat the last card's effect"""
        if last_card.is_number_card():
            value = last_card.get_value()
            if current_count % value == 0:
                return (current_count // value) >= 0
            else:
                return (current_count - value) >= 0
        
        elif last_card.is_ace():
            # Jack repeating ace uses minimum value (1)
            return (current_count - 1) >= 0
        
        elif last_card.rank == 'Q':
            try:
                if current_count < 10:
                    return False
                reversed_count = int(str(current_count)[::-1])
                return reversed_count < current_count and reversed_count >= 0
            except ValueError:
                return False
        
        elif last_card.rank == 'K':
            # Check if any divisor is available
            for divisor in range(2, current_count):
                if current_count % divisor == 0:
                    return True
            return False
        
        return False
    
    def has_playable_cards(self, current_count, last_card=None):
        """Check if player has any playable cards"""
        return len(self.get_playable_cards(current_count, last_card)) > 0
    
    def get_card_options(self, card, current_count):
        """Get available playing options for a specific card"""
        options = []
        
        if card.is_number_card():
            value = card.get_value()
            
            # Check division first (mandatory if possible)
            if current_count % value == 0:
                new_count = current_count // value
                options.append({
                    'action': 'divide',
                    'value': value,
                    'new_count': new_count,
                    'description': f"Divide by {value}: {current_count} ÷ {value} = {new_count} (MANDATORY)"
                })
            else:
                # Can only subtract if division is not possible
                new_count = current_count - value
                if new_count >= 0:
                    options.append({
                        'action': 'subtract',
                        'value': value,
                        'new_count': new_count,
                        'description': f"Subtract {value}: {current_count} - {value} = {new_count}"
                    })
        
        elif card.is_ace():
            # Ace options (1 or 11)
            for ace_value in [1, 11]:
                new_count = current_count - ace_value
                if new_count >= 0:
                    options.append({
                        'action': 'subtract',
                        'value': ace_value,
                        'new_count': new_count,
                        'description': f"Subtract {ace_value}: {current_count} - {ace_value} = {new_count}"
                    })
        
        elif card.rank == 'Q':
            # Queen reverses digits
            try:
                if current_count >= 10:
                    reversed_count = int(str(current_count)[::-1])
                    if reversed_count < current_count and reversed_count >= 0:
                        options.append({
                            'action': 'reverse',
                            'value': current_count,
                            'new_count': reversed_count,
                            'description': f"Reverse digits: {current_count} → {reversed_count}"
                        })
            except ValueError:
                pass
        
        elif card.rank == 'K':
            # King division options
            divisors = []
            for divisor in range(2, current_count):
                if current_count % divisor == 0:
                    divisors.append(divisor)
            
            # Sort divisors to show best options first
            divisors.sort()
            
            for divisor in divisors:
                new_count = current_count // divisor
                options.append({
                    'action': 'divide',
                    'value': divisor,
                    'new_count': new_count,
                    'description': f"Divide by {divisor}: {current_count} ÷ {divisor} = {new_count}"
                })
        
        elif card.rank == 'J':
            # Jack repeats previous card - show what it would do
            options.append({
                'action': 'repeat',
                'value': None,
                'new_count': None,  # Would need last card to calculate
                'description': f"Repeat effect of previous card"
            })
        
        return options
    
    def get_statistics(self):
        """Get player statistics"""
        return {
            'name': self.name,
            'is_human': self.is_human,
            'score': self.score,
            'rounds_won': self.rounds_won,
            'cards_in_hand': len(self.hand),
            'cards_played_this_round': self.cards_played_this_round,
            'total_cards_played': self.total_cards_played,
            'is_active': self.is_active
        }
    
    def __str__(self):
        """String representation of the player"""
        return f"{self.name} ({'Human' if self.is_human else 'Computer'}) - Score: {self.score}, Cards: {len(self.hand)}"
    
    def __repr__(self):
        """Object representation of the player"""
        return f"Player('{self.name}', is_human={self.is_human}, score={self.score}, cards={len(self.hand)})"