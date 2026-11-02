"""
Game manager for Limbo GUI game - handles game logic and state
Updated with complete Limbo rules including card drawing mechanics
"""

from .deck import Deck
from .player import Player
from .card import Card
from .ai_player import AIPlayer
import random

class GameManager:
    """Manages game state and logic for Limbo card game"""
    
    def __init__(self):
        """Initialize game manager"""
        self.deck = Deck()
        self.players = []
        self.current_player_index = 0
        self.game_mode = 'human_vs_human'  # or 'human_vs_computer'
        self.ai_difficulty = 'Medium'
        
        # Game state
        self.current_count = 101
        self.cards_played = 0
        self.last_card = None
        self.round_multiplier = 1
        self.target_score = 200
        
        # Round state
        self.round_active = False
        self.game_active = False
        self.winner = None
        self.doubling_phase = False
        self.dealer_index = 0
        self.forced_draw_in_progress = False
        
        # Callbacks for GUI updates
        self.on_game_state_changed = None
        self.on_card_played = None
        self.on_round_ended = None
        self.on_game_ended = None
        self.on_card_drawn = None
        
    def setup_game(self, player1_name, player2_name, target_score=200, 
                   game_mode='human_vs_human', ai_difficulty='Medium'):
        """Setup a new game with specified parameters"""
        self.target_score = target_score
        self.game_mode = game_mode
        self.ai_difficulty = ai_difficulty
        
        # Create players
        self.players = []
        self.players.append(Player(player1_name, is_human=True))
        
        if game_mode == 'human_vs_computer':
            self.players.append(AIPlayer(player2_name, ai_difficulty))
        else:
            self.players.append(Player(player2_name, is_human=True))
        
        # Reset game state
        self.reset_game()
        self.game_active = True
        
        # Notify GUI
        self._notify_game_state_changed()
    
    def reset_game(self):
        """Reset game to initial state"""
        for player in self.players:
            player.reset_score()
            player.clear_hand()
            player.reset_round_stats()
        
        self.current_count = 101
        self.cards_played = 0
        self.last_card = None
        self.round_multiplier = 1
        self.round_active = False
        self.winner = None
        self.doubling_phase = False
        self.dealer_index = 0
        self.current_player_index = 1  # Non-dealer starts
        self.forced_draw_in_progress = False
        
        self.deck.reset_and_shuffle()
    
    def start_new_round(self):
        """Start a new round"""
        # Reset round state
        self.current_count = 101
        self.cards_played = 0
        self.last_card = None
        self.round_multiplier = 1
        self.round_active = True
        self.forced_draw_in_progress = False
        
        # Clear hands and reset round stats
        for player in self.players:
            player.clear_hand()
            player.reset_round_stats()
        
        # Shuffle deck
        self.deck.reset_and_shuffle()
        
        # Deal cards (5 to each player)
        for _ in range(5):
            for player in self.players:
                card = self.deck.deal_card()
                if card:
                    player.add_card(card)
        
        # Set current player to non-dealer
        self.current_player_index = (self.dealer_index + 1) % 2
        
        # Start doubling phase
        self.doubling_phase = True
        
        self._notify_game_state_changed()
        return True
    
    def handle_doubling(self, player_index, wants_to_double):
        """Handle doubling/redoubling phase"""
        if not self.doubling_phase:
            return False
        
        if wants_to_double:
            if self.round_multiplier == 1:
                self.round_multiplier = 2
                # Now dealer can redouble
                if player_index != self.dealer_index:
                    # Switch to dealer for redouble decision
                    self.current_player_index = self.dealer_index
                    self._notify_game_state_changed()
                    return True
            elif self.round_multiplier == 2:
                self.round_multiplier = 4
        
        # End doubling phase and start actual game
        self.doubling_phase = False
        self.current_player_index = (self.dealer_index + 1) % 2  # Non-dealer starts
        self.play_starting_card()
        
        self._notify_game_state_changed()
        return True
    
    def skip_doubling(self):
        """Skip the doubling phase entirely"""
        self.doubling_phase = False
        self.current_player_index = (self.dealer_index + 1) % 2
        self.play_starting_card()
        self._notify_game_state_changed()
    
    def play_starting_card(self):
        """Dealer plays the starting card from deck"""
        if not self.deck:
            return False
        
        starting_card = self.deck.deal_card()
        if not starting_card:
            return False
        
        self.last_card = starting_card
        self.cards_played = 1
        
        # Apply starting card effect based on correct rules
        if starting_card.is_face_card():
            # Face cards keep count at 101 for starting position
            pass
        elif starting_card.is_ace():
            # Aces as starter subtract 1 (minimum value)
            self.current_count -= 1
        else:
            # Number cards subtract their value
            value = starting_card.get_value()
            self.current_count -= value
        
        self._notify_card_played(self.dealer_index, starting_card, 'starting')
        self._notify_game_state_changed()
        return True
    
    def can_player_play(self, player_index):
        """Check if specified player can play any card"""
        if not self.round_active or self.doubling_phase:
            return False
        
        if player_index != self.current_player_index:
            return False
        
        player = self.players[player_index]
        return player.has_playable_cards(self.current_count, self.last_card)
    
    def get_playable_cards(self, player_index):
        """Get list of playable cards for specified player"""
        if not self.can_player_play(player_index):
            return []
        
        player = self.players[player_index]
        return player.get_playable_cards(self.current_count, self.last_card)
    
    def play_card(self, player_index, card_index, action_data=None):
        """Play a card from player's hand"""
        if not self.can_player_play(player_index) and not self.forced_draw_in_progress:
            return False
        
        player = self.players[player_index]
        
        try:
            # Check if the card can be played first
            card = player.get_card_at_index(card_index)
            if not self._can_play_card_with_action(card, action_data):
                return False
            
            # Remove card from hand
            card = player.play_card(card_index)
            success = self._apply_card_effect(card, action_data)
            
            if success:
                self.last_card = card
                self.cards_played += 1
                self.forced_draw_in_progress = False  # Reset draw flag
                
                # Check win conditions
                if self.current_count == 0:
                    self._handle_win(player_index)
                elif not player.has_cards():
                    self._handle_player_out_of_cards(player_index)
                else:
                    # Switch to next player
                    self._switch_to_next_player()
                
                self._notify_card_played(player_index, card, action_data)
                self._notify_game_state_changed()
                return True
            else:
                # Return card to hand if play failed
                player.add_card(card)
                return False
                
        except (IndexError, ValueError):
            return False
    
    def _switch_to_next_player(self):
        """Switch to the next player with card drawing logic"""
        self.current_player_index = (self.current_player_index + 1) % 2
        
        # Check if new current player can play
        if not self.can_player_play(self.current_player_index):
            # Player must draw from stock before forfeiting
            self._handle_forced_draw()
        else:
            self._notify_game_state_changed()
    
    def _handle_forced_draw(self):
        """Handle when player must draw from stock because they can't play"""
        current_player = self.get_current_player()
        
        if self.deck.is_empty():
            # No cards to draw - current player forfeits
            winner_index = (self.current_player_index + 1) % 2
            self._end_round(winner_index)
            return
        
        # Draw card from stock
        drawn_card = self.deck.deal_card()
        current_player.add_card(drawn_card)
        
        # Notify GUI about the draw
        if self.on_card_drawn:
            self.on_card_drawn(self.current_player_index, drawn_card)
        
        if current_player.can_play_card(drawn_card, self.current_count, self.last_card):
            # Must immediately play the drawn card
            self.forced_draw_in_progress = True
            self._force_play_drawn_card(drawn_card)
        else:
            # Keep card and end turn (pass to opponent)
            self.forced_draw_in_progress = False
            self._switch_to_next_player()
    
    def _force_play_drawn_card(self, card):
        """Force immediate play of drawn card if it's playable"""
        current_player = self.get_current_player()
        
        # Find the card in player's hand
        try:
            card_index = current_player.hand.index(card)
            
            # Get action data if needed (for Aces, Kings)
            action_data = self._get_auto_action_data(card)
            
            # Play the card
            success = self.play_card(self.current_player_index, card_index, action_data)
            
            if not success:
                # Fallback: remove from hand and apply effect manually
                current_player.hand.remove(card)
                success = self._apply_card_effect(card, action_data)
                if success:
                    self.last_card = card
                    self.cards_played += 1
                    self.forced_draw_in_progress = False
                    
                    # Check win conditions
                    if self.current_count == 0:
                        self._handle_win(self.current_player_index)
                    elif not current_player.has_cards():
                        self._handle_player_out_of_cards(self.current_player_index)
                    else:
                        self._switch_to_next_player()
                    
                    self._notify_card_played(self.current_player_index, card, action_data)
                    self._notify_game_state_changed()
                else:
                    # Re-add card if effect failed
                    current_player.add_card(card)
                    self.forced_draw_in_progress = False
                    self._switch_to_next_player()
                
        except (ValueError, IndexError):
            # Error handling - end turn
            self.forced_draw_in_progress = False
            self._switch_to_next_player()
    
    def _get_auto_action_data(self, card):
        """Get automatic action data for forced card play"""
        if card.is_ace():
            # Choose the value that keeps count >= 0
            if self.current_count >= 11:
                return {'value': 11}  # Prefer larger reduction
            else:
                return {'value': 1}
        
        elif card.rank == 'K':
            # Choose smallest valid divisor for King
            for divisor in range(2, self.current_count):
                if self.current_count % divisor == 0:
                    return {'value': divisor}
        
        return None
    
    def draw_stock_card(self, player_index):
        """Public method to draw from stock (for GUI integration)"""
        if player_index != self.current_player_index:
            return False
        
        if not self.can_player_play(player_index):
            self._handle_forced_draw()
            return True
        
        return False  # Player has playable cards, can't draw
    
    def _can_play_card_with_action(self, card, action_data):
        """Check if a card can be played with the given action"""
        if not card:
            return False
        
        # Simulate the effect to check validity
        test_count = self.current_count
        
        if card.is_number_card():
            value = card.get_value()
            # Check if division is mandatory
            if test_count % value == 0:
                # Division is mandatory - can only divide
                new_count = test_count // value
                return new_count >= 0
            else:
                # Can only subtract
                new_count = test_count - value
                return new_count >= 0
        
        elif card.is_ace():
            # Check the requested ace value
            ace_value = 1  # Default
            if action_data and 'value' in action_data:
                ace_value = action_data['value']
            return test_count - ace_value >= 0
        
        elif card.rank == 'J':
            # Jack requires a previous card
            return self.last_card is not None
        
        elif card.rank == 'Q':
            # Queen can only be played if reversal reduces count
            try:
                if test_count < 10:
                    return False
                reversed_count = int(str(test_count)[::-1])
                return reversed_count < test_count and reversed_count >= 0
            except ValueError:
                return False
        
        elif card.rank == 'K':
            # King needs a valid divisor
            if action_data and 'value' in action_data:
                divisor = action_data['value']
                return (divisor > 1 and divisor < test_count and 
                       test_count % divisor == 0)
            else:
                # Check if any divisor is available
                for divisor in range(2, test_count):
                    if test_count % divisor == 0:
                        return True
                return False
        
        return False
    
    def _apply_card_effect(self, card, action_data):
        """Apply the effect of playing a card"""
        old_count = self.current_count
        
        try:
            if card.is_number_card():
                return self._apply_number_card(card, action_data)
            elif card.is_ace():
                return self._apply_ace_card(card, action_data)
            elif card.rank == 'J':
                return self._apply_jack_card(card)
            elif card.rank == 'Q':
                return self._apply_queen_card(card)
            elif card.rank == 'K':
                return self._apply_king_card(card, action_data)
            
            return False
            
        except Exception:
            self.current_count = old_count  # Restore on error
            return False
    
    def _apply_number_card(self, card, action_data):
        """Apply number card effect - DIVISION IS MANDATORY if possible"""
        value = card.get_value()
        
        # Division is mandatory if possible (key Limbo rule!)
        if self.current_count % value == 0:
            self.current_count //= value
        else:
            # Can only subtract if division is not possible
            new_count = self.current_count - value
            if new_count >= 0:
                self.current_count = new_count
            else:
                return False
        
        return True
    
    def _apply_ace_card(self, card, action_data):
        """Apply Ace card effect"""
        ace_value = 1  # Default
        
        if action_data and 'value' in action_data:
            ace_value = action_data['value']
        
        # Aces can only subtract (never divide)
        new_count = self.current_count - ace_value
        if new_count >= 0:
            self.current_count = new_count
            return True
        
        return False
    
    def _apply_jack_card(self, card):
        """Apply Jack card effect (repeat last card)"""
        if not self.last_card:
            return False
        
        # Apply the same effect as last card
        if self.last_card.is_number_card():
            return self._apply_number_card(self.last_card, None)
        elif self.last_card.is_ace():
            # For Jack repeating Ace, use minimum value (1)
            return self._apply_ace_card(self.last_card, {'value': 1})
        elif self.last_card.rank == 'Q':
            return self._apply_queen_card(self.last_card)
        elif self.last_card.rank == 'K':
            # For King, use smallest available divisor
            for divisor in range(2, self.current_count):
                if self.current_count % divisor == 0:
                    self.current_count //= divisor
                    return True
            return False
        
        return False
    
    def _apply_queen_card(self, card):
        """Apply Queen card effect (reverse digits)"""
        try:
            if self.current_count < 10:
                return False
            
            reversed_count = int(str(self.current_count)[::-1])
            # Queen can only be played if it reduces the count
            if reversed_count < self.current_count and reversed_count >= 0:
                self.current_count = reversed_count
                return True
        except ValueError:
            pass
        
        return False
    
    def _apply_king_card(self, card, action_data):
        """Apply King card effect (divide by chosen divisor)"""
        divisor = 2  # Default
        
        if action_data and 'value' in action_data:
            divisor = action_data['value']
        else:
            # Choose smallest available divisor
            for d in range(2, self.current_count):
                if self.current_count % d == 0:
                    divisor = d
                    break
        
        if (divisor > 1 and divisor <= self.current_count and 
            self.current_count % divisor == 0):
            self.current_count //= divisor
            return True
        
        return False
    
    def _handle_win(self, player_index):
        """Handle when a player wins by reaching exactly 0"""
        self._end_round(player_index)
    
    def _handle_player_out_of_cards(self, player_index):
        """Handle when a player runs out of cards"""
        # Player who played their last card wins (since they made a legal move)
        self._end_round(player_index)
    
    def _end_round(self, winner_index):
        """End the current round with specified winner"""
        if not self.round_active:
            return
        
        self.round_active = False
        winner = self.players[winner_index]
        loser = self.players[1 - winner_index]
        
        # Calculate scores according to Limbo rules
        # Winner: 10 × number of cards played (including starter) × multiplier
        # Loser: 10 × final count value (no multiplier for loser)
        winner_points = 10 * self.cards_played * self.round_multiplier
        loser_points = 10 * self.current_count  # No multiplier for loser
        
        winner.add_score(winner_points)
        winner.add_round_win()
        loser.add_score(loser_points)
        
        # Check for game end
        if winner.score >= self.target_score:
            self.winner = winner
            self.game_active = False
            self._notify_game_ended(winner)
        else:
            # Prepare for next round
            self.dealer_index = (self.dealer_index + 1) % 2
            self._notify_round_ended(winner, winner_points, loser_points)
    
    def get_game_state(self):
        """Get current game state"""
        return {
            'current_count': self.current_count,
            'cards_played': self.cards_played,
            'last_card': self.last_card,
            'current_player_index': self.current_player_index,
            'round_multiplier': self.round_multiplier,
            'target_score': self.target_score,
            'round_active': self.round_active,
            'game_active': self.game_active,
            'doubling_phase': self.doubling_phase,
            'dealer_index': self.dealer_index,
            'deck_size': len(self.deck),
            'forced_draw_in_progress': self.forced_draw_in_progress,
            'players': [player.get_statistics() for player in self.players]
        }
    
    def get_current_player(self):
        """Get current player"""
        if 0 <= self.current_player_index < len(self.players):
            return self.players[self.current_player_index]
        return None
    
    def get_player(self, index):
        """Get player by index"""
        if 0 <= index < len(self.players):
            return self.players[index]
        return None
    
    def get_ai_move(self):
        """Get AI player's move (if current player is AI)"""
        current_player = self.get_current_player()
        if current_player and not current_player.is_human:
            if hasattr(current_player, 'get_best_move'):
                return current_player.get_best_move(self.current_count, self.last_card)
        return None
    
    # Callback setters
    def set_game_state_callback(self, callback):
        """Set callback for game state changes"""
        self.on_game_state_changed = callback
    
    def set_card_played_callback(self, callback):
        """Set callback for card played events"""
        self.on_card_played = callback
    
    def set_round_ended_callback(self, callback):
        """Set callback for round ended events"""
        self.on_round_ended = callback
    
    def set_game_ended_callback(self, callback):
        """Set callback for game ended events"""
        self.on_game_ended = callback
    
    def set_card_drawn_callback(self, callback):
        """Set callback for card drawn events"""
        self.on_card_drawn = callback
    
    # Notification methods
    def _notify_game_state_changed(self):
        """Notify GUI of game state change"""
        if self.on_game_state_changed:
            self.on_game_state_changed(self.get_game_state())
    
    def _notify_card_played(self, player_index, card, action_data):
        """Notify GUI of card played"""
        if self.on_card_played:
            self.on_card_played(player_index, card, action_data)
    
    def _notify_round_ended(self, winner, winner_points, loser_points):
        """Notify GUI of round end"""
        if self.on_round_ended:
            self.on_round_ended(winner, winner_points, loser_points)
    
    def _notify_game_ended(self, winner):
        """Notify GUI of game end"""
        if self.on_game_ended:
            self.on_game_ended(winner)