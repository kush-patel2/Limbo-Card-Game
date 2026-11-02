"""
Deck class for Limbo GUI game
"""

import random
from .card import Card

class Deck:
    """Represents a deck of playing cards"""
    
    def __init__(self):
        """Initialize a standard 52-card deck"""
        self.cards = []
        self.dealt_cards = []  # Keep track of dealt cards for GUI purposes
        self.create_deck()
    
    def create_deck(self):
        """Create a standard 52-card deck"""
        self.cards = []
        self.dealt_cards = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.cards.append(Card(suit, rank))
    
    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.cards)
    
    def deal_card(self):
        """Deal one card from the top of the deck"""
        if not self.cards:
            return None
        
        card = self.cards.pop()
        self.dealt_cards.append(card)
        return card
    
    def deal_multiple_cards(self, count):
        """Deal multiple cards at once"""
        dealt = []
        for _ in range(min(count, len(self.cards))):
            card = self.deal_card()
            if card:
                dealt.append(card)
        return dealt
    
    def is_empty(self):
        """Check if the deck is empty"""
        return len(self.cards) == 0
    
    def cards_remaining(self):
        """Get the number of cards remaining in the deck"""
        return len(self.cards)
    
    def total_cards_dealt(self):
        """Get the number of cards that have been dealt"""
        return len(self.dealt_cards)
    
    def peek_top_card(self):
        """Look at the top card without removing it"""
        if not self.cards:
            return None
        return self.cards[-1]
    
    def peek_multiple_cards(self, count):
        """Look at multiple top cards without removing them"""
        if count <= 0:
            return []
        
        peek_count = min(count, len(self.cards))
        return self.cards[-peek_count:][::-1]  # Return in dealing order
    
    def reset(self):
        """Reset the deck to a full 52-card deck"""
        self.create_deck()
    
    def reset_and_shuffle(self):
        """Reset and shuffle the deck"""
        self.reset()
        self.shuffle()
    
    def get_dealt_cards(self):
        """Get list of all dealt cards (for game state tracking)"""
        return self.dealt_cards.copy()
    
    def get_remaining_cards(self):
        """Get list of remaining cards in deck"""
        return self.cards.copy()
    
    def add_card_to_bottom(self, card):
        """Add a card to the bottom of the deck"""
        if isinstance(card, Card):
            self.cards.insert(0, card)
            # Remove from dealt cards if it was there
            if card in self.dealt_cards:
                self.dealt_cards.remove(card)
    
    def add_cards_to_bottom(self, cards):
        """Add multiple cards to the bottom of the deck"""
        for card in cards:
            self.add_card_to_bottom(card)
    
    def remove_card(self, card):
        """Remove a specific card from the deck (if present)"""
        if card in self.cards:
            self.cards.remove(card)
            return True
        return False
    
    def contains_card(self, card):
        """Check if deck contains a specific card"""
        return card in self.cards
    
    def get_cards_by_suit(self, suit):
        """Get all remaining cards of a specific suit"""
        return [card for card in self.cards if card.suit == suit]
    
    def get_cards_by_rank(self, rank):
        """Get all remaining cards of a specific rank"""
        return [card for card in self.cards if card.rank == rank]
    
    def get_face_cards(self):
        """Get all remaining face cards"""
        return [card for card in self.cards if card.is_face_card()]
    
    def get_number_cards(self):
        """Get all remaining number cards"""
        return [card for card in self.cards if card.is_number_card()]
    
    def get_aces(self):
        """Get all remaining aces"""
        return [card for card in self.cards if card.is_ace()]
    
    def get_deck_composition(self):
        """Get a summary of deck composition for debugging"""
        composition = {
            'total_cards': len(self.cards),
            'cards_dealt': len(self.dealt_cards),
            'by_suit': {},
            'by_rank': {},
            'face_cards': len(self.get_face_cards()),
            'number_cards': len(self.get_number_cards()),
            'aces': len(self.get_aces())
        }
        
        # Count by suit
        for suit in Card.SUITS:
            composition['by_suit'][suit] = len(self.get_cards_by_suit(suit))
        
        # Count by rank
        for rank in Card.RANKS:
            composition['by_rank'][rank] = len(self.get_cards_by_rank(rank))
        
        return composition
    
    def __str__(self):
        """String representation of the deck"""
        return f"Deck with {len(self.cards)} cards remaining, {len(self.dealt_cards)} dealt"
    
    def __len__(self):
        """Get the number of cards remaining in the deck"""
        return len(self.cards)
    
    def __bool__(self):
        """Check if deck has any cards"""
        return len(self.cards) > 0
    
    def __iter__(self):
        """Iterate over remaining cards in deck"""
        return iter(self.cards)