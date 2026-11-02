"""
AI Player class for Limbo GUI game
Enhanced with card drawing mechanics and improved doubling decisions
"""

import random
from .player import Player

class AIPlayer(Player):
    """AI Player that can make intelligent decisions including drawing and doubling"""
    
    def __init__(self, name, difficulty='Medium'):
        """Initialize AI player with difficulty level"""
        super().__init__(name, is_human=False)
        self.difficulty = difficulty
        self.thinking_time = self._get_thinking_time()
        
        # AI personality based on difficulty
        self.aggression = self._get_aggression_level()
        self.calculation_depth = self._get_calculation_depth()
        self.mistake_probability = self._get_mistake_probability()
        self.doubling_threshold = self._get_doubling_threshold()
        
        # Memory for strategic decisions
        self.cards_seen = set()
        self.opponent_likely_cards = []
        
    def _get_thinking_time(self):
        """Get thinking time based on difficulty"""
        times = {'Easy': 0.8, 'Medium': 1.5, 'Hard': 2.2}
        return times.get(self.difficulty, 1.5)
    
    def _get_aggression_level(self):
        """Get aggression level (tendency to take risks)"""
        levels = {'Easy': 0.3, 'Medium': 0.5, 'Hard': 0.7}
        return levels.get(self.difficulty, 0.5)
    
    def _get_calculation_depth(self):
        """Get how many moves ahead AI calculates"""
        depths = {'Easy': 1, 'Medium': 2, 'Hard': 4}
        return depths.get(self.difficulty, 2)
    
    def _get_mistake_probability(self):
        """Get probability of making suboptimal moves"""
        probs = {'Easy': 0.25, 'Medium': 0.08, 'Hard': 0.03}
        return probs.get(self.difficulty, 0.08)
    
    def _get_doubling_threshold(self):
        """Get hand strength threshold for doubling decisions"""
        thresholds = {'Easy': 0.8, 'Medium': 0.65, 'Hard': 0.55}
        return thresholds.get(self.difficulty, 0.65)
    
    def get_best_move(self, current_count, last_card=None):
        """Get the best move for current game state"""
        playable_cards = self.get_playable_cards(current_count, last_card)
        
        if not playable_cards:
            return None
        
        # Introduce mistakes based on difficulty
        if random.random() < self.mistake_probability:
            return self._get_random_move(playable_cards, current_count)
        
        # Calculate best move based on difficulty
        if self.difficulty == 'Easy':
            return self._get_easy_move(playable_cards, current_count)
        elif self.difficulty == 'Medium':
            return self._get_medium_move(playable_cards, current_count, last_card)
        else:  # Hard
            return self._get_hard_move(playable_cards, current_count, last_card)
    
    def _get_random_move(self, playable_cards, current_count):
        """Get a random playable move"""
        if not playable_cards:
            return None
        
        card_index, card = random.choice(playable_cards)
        return {
            'card_index': card_index,
            'card': card,
            'action_data': self._get_default_action_data(card, current_count)
        }
    
    def _get_easy_move(self, playable_cards, current_count):
        """Easy AI - basic strategy"""
        best_move = None
        best_score = float('-inf')
        
        for card_index, card in playable_cards:
            score = self._evaluate_card_simple(card, current_count)
            
            if score > best_score:
                best_score = score
                best_move = {
                    'card_index': card_index,
                    'card': card,
                    'action_data': self._get_default_action_data(card, current_count)
                }
        
        return best_move
    
    def _get_medium_move(self, playable_cards, current_count, last_card):
        """Medium AI - considers opponent's options and basic strategy"""
        best_move = None
        best_score = float('-inf')
        
        for card_index, card in playable_cards:
            # Evaluate move considering future game state
            score = self._evaluate_card_medium(card, current_count, last_card)
            
            if score > best_score:
                best_score = score
                best_move = {
                    'card_index': card_index,
                    'card': card,
                    'action_data': self._get_optimal_action_data(card, current_count)
                }
        
        return best_move
    
    def _get_hard_move(self, playable_cards, current_count, last_card):
        """Hard AI - advanced strategy with deep lookahead"""
        best_move = None
        best_score = float('-inf')
        
        for card_index, card in playable_cards:
            # Deep evaluation considering multiple moves ahead
            score = self._evaluate_card_hard(card, current_count, last_card)
            
            # Add drawing scenario analysis
            score += self._evaluate_drawing_scenarios(card, current_count)
            
            if score > best_score:
                best_score = score
                best_move = {
                    'card_index': card_index,
                    'card': card,
                    'action_data': self._get_optimal_action_data(card, current_count)
                }
        
        return best_move
    
    def _evaluate_drawing_scenarios(self, card, current_count):
        """Evaluate how this move affects drawing scenarios"""
        new_count = self._calculate_new_count(card, current_count)
        score = 0
        
        # Bonus for moves that might force opponent to draw
        if self._likely_forces_opponent_draw(new_count):
            score += 100
        
        # Penalty for moves that might force us to draw later
        if self._might_force_self_draw(new_count):
            score -= 50
        
        return score
    
    def _likely_forces_opponent_draw(self, new_count):
        """Check if this count is likely to force opponent to draw"""
        # Hard AI tries to estimate opponent's hand capabilities
        if self.difficulty != 'Hard':
            return False
        
        # Prime numbers and other difficult positions
        difficult_counts = [1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        
        if new_count in difficult_counts:
            return True
        
        # Counts with very few divisor options
        if new_count > 1:
            divisors = [i for i in range(2, new_count) if new_count % i == 0]
            if len(divisors) <= 2:  # Very few options
                return True
        
        return False
    
    def _might_force_self_draw(self, new_count):
        """Check if this count might force us to draw later"""
        # Conservative check - avoid positions that limit our future options
        remaining_hand_strength = self._evaluate_remaining_hand_strength()
        
        if remaining_hand_strength < 0.3 and new_count < 20:
            return True
        
        return False
    
    def _evaluate_remaining_hand_strength(self):
        """Evaluate the strength of remaining cards in hand"""
        if not self.hand:
            return 0.0
        
        strength = 0.0
        for card in self.hand:
            if card.rank == 'K':
                strength += 1.0  # Kings are most flexible
            elif card.rank == 'Q':
                strength += 0.7  # Queens are situational but powerful
            elif card.is_ace():
                strength += 0.8  # Aces are very flexible
            elif card.rank == 'J':
                strength += 0.3  # Jacks depend on last card
            elif card.is_number_card():
                value = card.get_value()
                if value in [2, 3, 5]:  # Good small divisors
                    strength += 0.6
                elif value in [7]:  # Prime number
                    strength += 0.5
                else:
                    strength += 0.4
        
        return strength / len(self.hand)
    
    def _evaluate_card_simple(self, card, current_count):
        """Simple card evaluation for easy AI"""
        score = 0
        new_count = self._calculate_new_count(card, current_count)
        
        # Prefer moves that reduce count significantly
        reduction = current_count - new_count
        score = reduction * 2
        
        # Small bonus for reaching target numbers
        if new_count == 0:
            score += 1000  # Winning move
        elif new_count <= 3:
            score += 50   # Very good
        elif new_count <= 10:
            score += 20   # Good
        
        return score
    
    def _evaluate_card_medium(self, card, current_count, last_card):
        """Medium card evaluation considering opponent options"""
        base_score = self._evaluate_card_simple(card, current_count)
        
        # Calculate resulting count
        new_count = self._calculate_new_count(card, current_count)
        
        # Consider how many options opponent will have
        opponent_options = self._count_opponent_options(new_count)
        
        # Prefer moves that give opponent fewer options
        option_penalty = opponent_options * 8
        
        # Bonus for creating strategic positions
        strategy_bonus = 0
        if self._creates_trap(new_count):
            strategy_bonus += 75
        
        # Bonus for getting close to winning
        if new_count <= 5:
            strategy_bonus += 40
        elif new_count <= 15:
            strategy_bonus += 20
        
        # Penalty for giving opponent easy positions
        if new_count in [4, 6, 8, 9, 10, 12, 15, 16, 18, 20]:
            strategy_bonus -= 30
        
        return base_score - option_penalty + strategy_bonus
    
    def _evaluate_card_hard(self, card, current_count, last_card):
        """Advanced card evaluation with deep lookahead"""
        medium_score = self._evaluate_card_medium(card, current_count, last_card)
        
        # Calculate new count after this move
        new_count = self._calculate_new_count(card, current_count)
        
        # Advanced strategies
        strategy_bonus = 0
        
        # Multi-move lookahead
        strategy_bonus += self._evaluate_lookahead(new_count, depth=self.calculation_depth)
        
        # Endgame strategy
        if new_count <= 25:
            strategy_bonus += self._evaluate_endgame_move(card, new_count) * 1.5
        
        # Pattern recognition bonus
        if self._follows_good_pattern(card, current_count):
            strategy_bonus += 35
        
        # Advanced trap creation
        if self._creates_powerful_trap(new_count):
            strategy_bonus += 100
        
        # Hand management bonus
        strategy_bonus += self._evaluate_hand_management(card)
        
        return medium_score + strategy_bonus
    
    def _evaluate_lookahead(self, count, depth):
        """Evaluate positions multiple moves ahead"""
        if depth <= 0 or count <= 0:
            return 0
        
        # Simplified lookahead - check if opponent has good responses
        opponent_best_response = self._estimate_opponent_best_response(count)
        
        if opponent_best_response:
            # Recursively evaluate the position after opponent's response
            return -self._evaluate_lookahead(opponent_best_response, depth - 1) * 0.7
        
        return 0
    
    def _estimate_opponent_best_response(self, count):
        """Estimate what the opponent's best response might be"""
        # Simplified estimation based on common good moves
        good_moves = []
        
        # Check common divisors
        for divisor in [2, 3, 4, 5, 6, 8, 10]:
            if count % divisor == 0:
                result = count // divisor
                if result >= 0:
                    good_moves.append(result)
        
        # Check subtraction options
        for subtract in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
            result = count - subtract
            if result >= 0:
                good_moves.append(result)
        
        # Return the best looking option
        if good_moves:
            return min(good_moves)  # Assume opponent wants to minimize count
        
        return None
    
    def _evaluate_hand_management(self, card):
        """Evaluate how playing this card affects hand management"""
        bonus = 0
        
        # Don't waste powerful cards early
        if card.rank in ['K', 'Q'] and len(self.hand) > 3:
            # Check if we have simpler alternatives
            simple_alternatives = [c for c in self.hand if c.is_number_card()]
            if simple_alternatives:
                bonus -= 25  # Penalty for wasting good cards
        
        # Use number cards when we can divide
        if card.is_number_card():
            bonus += 10  # Small bonus for using number cards
        
        return bonus
    
    def _calculate_new_count(self, card, current_count):
        """Calculate the new count after playing this card"""
        if card.is_number_card():
            value = card.get_value()
            # Division is mandatory if possible
            if current_count % value == 0:
                return current_count // value
            else:
                return current_count - value
        
        elif card.is_ace():
            # Choose optimal Ace value
            if current_count >= 11:
                # Consider both options
                option1 = current_count - 1
                option11 = current_count - 11
                
                # Prefer the option that creates a better strategic position
                if self._creates_trap(option11) and option11 >= 0:
                    return option11
                elif self._creates_trap(option1) and option1 >= 0:
                    return option1
                elif option11 >= 0:
                    return option11  # Prefer larger reduction
                else:
                    return option1
            else:
                return max(0, current_count - 1)
        
        elif card.rank == 'Q':
            try:
                if current_count >= 10:
                    reversed_count = int(str(current_count)[::-1])
                    if reversed_count < current_count and reversed_count >= 0:
                        return reversed_count
            except ValueError:
                pass
            return current_count  # No change if can't reverse
        
        elif card.rank == 'K':
            # Find best divisor
            best_result = current_count
            for divisor in range(2, current_count):
                if current_count % divisor == 0:
                    result = current_count // divisor
                    if self._creates_trap(result) or result < best_result:
                        best_result = result
            return best_result
        
        elif card.rank == 'J':
            # Jack effect depends on last card - simplified here
            return max(0, current_count - 3)  # Rough estimation
        
        return current_count
    
    def _count_opponent_options(self, count):
        """Estimate how many options opponent will have"""
        options = 0
        
        # Check number cards
        for value in range(2, 11):
            if count % value == 0 or count - value >= 0:
                options += 1
        
        # Aces
        if count >= 1:
            options += 1
        
        # Queen (if count can be meaningfully reversed)
        if count >= 10:
            try:
                reversed_count = int(str(count)[::-1])
                if reversed_count < count:
                    options += 1
            except ValueError:
                pass
        
        # King (if any divisors exist)
        for divisor in range(2, min(count, 11)):  # Check reasonable divisors
            if count % divisor == 0:
                options += 1
                break
        
        return options
    
    def _creates_trap(self, count):
        """Check if this count is difficult for opponent"""
        # Prime numbers are good traps
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        if count in primes:
            return True
        
        # Very small numbers (1-3) are often good
        if count <= 3:
            return True
        
        return False
    
    def _creates_powerful_trap(self, count):
        """Check if this creates an especially difficult position"""
        # Winning positions
        if count == 0:
            return True
        
        # Numbers with very few options
        if count in [1, 2, 3]:
            return True
        
        # Large primes
        large_primes = [17, 19, 23, 29, 31, 37, 41, 43, 47]
        if count in large_primes:
            return True
        
        return False
    
    def _evaluate_endgame_move(self, card, new_count):
        """Evaluate moves in endgame situations"""
        bonus = 0
        
        # Massive bonus for winning move
        if new_count == 0:
            bonus += 2000
        
        # High bonus for forcing opponent into very difficult positions
        elif new_count == 1:
            bonus += 300  # Opponent must have Ace
        elif new_count in [2, 3]:
            bonus += 200  # Very limited options
        elif new_count in [5, 7]:
            bonus += 150  # Prime numbers
        elif new_count in [11, 13]:
            bonus += 120  # Larger primes
        
        # Penalty for giving opponent easy options
        elif new_count in [4, 6, 8, 9, 10, 12]:
            bonus -= 80
        
        return bonus
    
    def _follows_good_pattern(self, card, current_count):
        """Check if this follows a good strategic pattern"""
        # Prefer division over subtraction when possible (already handled by rules)
        if card.is_number_card():
            value = card.get_value()
            if current_count % value == 0:
                return True
        
        # Prefer using powerful cards (K, Q) when count is high
        if card.rank in ['Q', 'K'] and current_count > 40:
            return True
        
        # Prefer using Aces for fine control in endgame
        if card.is_ace() and current_count <= 25:
            return True
        
        return False
    
    def _get_default_action_data(self, card, current_count):
        """Get default action data for a card"""
        if card.is_ace():
            return {'value': 1}  # Default to 1
        elif card.rank == 'K':
            # Find first valid divisor
            for divisor in range(2, current_count):
                if current_count % divisor == 0:
                    return {'value': divisor}
        
        return {}
    
    def _get_optimal_action_data(self, card, current_count):
        """Get optimal action data for a card"""
        if card.is_ace():
            # Choose best Ace value strategically
            if current_count >= 11:
                val1_result = current_count - 1
                val11_result = current_count - 11
                
                # Prefer result that creates better strategic position
                if val11_result >= 0 and self._creates_trap(val11_result):
                    return {'value': 11}
                elif val1_result >= 0 and self._creates_trap(val1_result):
                    return {'value': 1}
                elif val11_result >= 0:
                    return {'value': 11}  # Prefer larger reduction
                else:
                    return {'value': 1}
            else:
                return {'value': 1}
        
        elif card.rank == 'K':
            # Choose best divisor strategically
            best_divisor = 2
            best_score = float('-inf')
            
            for divisor in range(2, current_count):
                if current_count % divisor == 0:
                    result = current_count // divisor
                    score = self._evaluate_king_result(result)
                    
                    if score > best_score:
                        best_score = score
                        best_divisor = divisor
            
            return {'value': best_divisor}
        
        return {}
    
    def _evaluate_king_result(self, result):
        """Evaluate the desirability of a King division result"""
        score = 0
        
        # Huge bonus for winning
        if result == 0:
            score += 2000
        
        # High bonus for creating traps
        elif self._creates_trap(result):
            score += 300
        
        # Bonus for small results in endgame
        elif result <= 10:
            score += 150
        
        # Penalty for giving opponent easy numbers
        elif result in [4, 6, 8, 9, 10, 12, 15, 16, 18, 20]:
            score -= 100
        
        return score
    
    def should_double(self, round_multiplier, game_state=None):
        """Decide whether to double based on difficulty and game state"""
        hand_strength = self._evaluate_hand_strength()
        
        if self.difficulty == 'Easy':
            # Easy AI rarely doubles, and makes poor decisions
            return random.random() < 0.15
        
        elif self.difficulty == 'Medium':
            # Medium AI doubles based on hand strength with some randomness
            threshold = self.doubling_threshold + random.uniform(-0.1, 0.1)
            
            # Consider game state
            if game_state:
                score_difference = self.score - game_state.get('players', [{}])[0].get('score', 0)
                
                # More likely to double when behind
                if score_difference < -30:
                    threshold -= 0.15
                elif score_difference > 30:
                    threshold += 0.1
            
            return hand_strength > threshold
        
        else:  # Hard
            # Hard AI makes sophisticated doubling decisions
            return self._strategic_doubling_decision(round_multiplier, game_state)
    
    def _strategic_doubling_decision(self, round_multiplier, game_state):
        """Make strategic doubling decision for hard AI"""
        hand_strength = self._evaluate_hand_strength()
        
        # Base threshold
        threshold = self.doubling_threshold
        
        # Adjust for round multiplier
        if round_multiplier == 1:
            # Initial doubling decision
            threshold = 0.6
        elif round_multiplier == 2:
            # Redoubling decision - much more conservative
            threshold = 0.8
        
        # Consider game state
        if game_state:
            players = game_state.get('players', [])
            if len(players) >= 2:
                my_score = players[1].get('score', 0)  # AI is typically player 2
                opponent_score = players[0].get('score', 0)
                score_difference = my_score - opponent_score
                
                # Adjust threshold based on score situation
                if score_difference < -50:
                    threshold -= 0.2  # More aggressive when behind
                elif score_difference < -20:
                    threshold -= 0.1
                elif score_difference > 50:
                    threshold += 0.15  # More conservative when ahead
                elif score_difference > 20:
                    threshold += 0.05
        
        # Factor in hand flexibility (can we handle drawing?)
        flexibility = self._evaluate_hand_flexibility()
        if flexibility < 0.3:
            threshold += 0.1  # More conservative with inflexible hands
        
        # Add slight randomness to avoid predictability
        threshold += random.uniform(-0.05, 0.05)
        
        return hand_strength > threshold
    
    def _evaluate_hand_strength(self):
        """Evaluate the overall strength of current hand"""
        if not self.hand:
            return 0.0
        
        strength = 0.0
        total_cards = len(self.hand)
        
        for card in self.hand:
            if card.rank == 'K':
                strength += 1.0  # Kings are most powerful
            elif card.rank == 'Q':
                strength += 0.85  # Queens are very useful
            elif card.is_ace():
                strength += 0.8   # Aces are flexible
            elif card.rank == 'J':
                strength += 0.4   # Jacks are situational
            elif card.is_number_card():
                value = card.get_value()
                if value in [2, 3, 5]:  # Good small divisors
                    strength += 0.7
                elif value in [7]:  # Prime number
                    strength += 0.6
                elif value in [4, 6, 8]:  # Decent divisors
                    strength += 0.5
                else:
                    strength += 0.4
        
        return strength / total_cards if total_cards > 0 else 0.0
    
    def _evaluate_hand_flexibility(self):
        """Evaluate how flexible the hand is for different situations"""
        if not self.hand:
            return 0.0
        
        flexibility = 0.0
        
        # Count flexible cards
        flexible_cards = 0
        for card in self.hand:
            if card.rank in ['K', 'Q', 'A']:  # Very flexible
                flexible_cards += 1
                flexibility += 1.0
            elif card.rank == 'J':  # Somewhat flexible
                flexible_cards += 0.5
                flexibility += 0.5
            elif card.is_number_card():
                value = card.get_value()
                if value <= 5:  # Small numbers are more flexible
                    flexibility += 0.6
                else:
                    flexibility += 0.3
        
        return flexibility / len(self.hand)
    
    def update_seen_cards(self, card):
        """Update the list of cards that have been seen"""
        self.cards_seen.add(card)
    
    def reset_round_memory(self):
        """Reset memory for a new round"""
        self.cards_seen.clear()
        self.opponent_likely_cards.clear()
    
    def reset_round_stats(self):
        """Reset round-specific statistics"""
        super().reset_round_stats()
        self.reset_round_memory()