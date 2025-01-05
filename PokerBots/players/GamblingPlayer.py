import random
import pokerkit
import treys
from PokerBots.players.BasePlayer import BasePlayer

class GamblingPlayer(BasePlayer):
    """
    A poker player that uses Monte-Carlo Simulation to determine when to go all-in.
    """

    def __init__(self, name: str = "NPC", win_rate_threshold: float = 0.9):
        super().__init__(name=name)
        self.win_rate_threshold = win_rate_threshold

        self.__cards_treys = [
            treys.Card.new(card) for card in (
                "2c", "2d", "2h", "2s", "3c", "3d", "3h", "3s", "4c", "4d", "4h", "4s",
                "5c", "5d", "5h", "5s", "6c", "6d", "6h", "6s", "7c", "7d", "7h", "7s",
                "8c", "8d", "8h", "8s", "9c", "9d", "9h", "9s", "Tc", "Td", "Th", "Ts",
                "Jc", "Jd", "Jh", "Js", "Qc", "Qd", "Qh", "Qs", "Kc", "Kd", "Kh", "Ks",
                "Ac", "Ad", "Ah", "As"
            )
        ]

    def play(self, valid_actions: dict[str, float], state: pokerkit.State) -> tuple[str, float]:

        hole_cards = state.hole_cards[state.actor_index]
        board_cards = [x[0] for x in state.board_cards]

        n_active_players = state.player_count

        if "complete_bet_or_raise_to" in valid_actions:
            win_rate: float = self.__compute_win_rate_using_monte_carlo_simulation(
                hole_cards=hole_cards,
                board_cards=board_cards,
                n_players=n_active_players,
                n_simulations=100,
            )
            if win_rate >= self.win_rate_threshold:
                return "complete_bet_or_raise_to", valid_actions["complete_bet_or_raise_to"][1]
            
        if valid_actions.get("check_or_call") == 0:
            return "check_or_call", 0

        return "fold", 0.0

    def __compute_win_rate_using_monte_carlo_simulation(
        self, hole_cards: list[pokerkit.Card], board_cards: list[pokerkit.Card], n_players: int, n_simulations: int
    ) -> float:
        """
        Estimate the win rate using Monte Carlo simulation.

        Args:
            hole_cards: The two cards in the player's hand.
            board_cards: The cards currently on the board.
            n_players: The number of active players.
            n_simulations: The number of simulations to run.

        Returns:
            The estimated win rate (a float between 0 and 1).
        """
        # Prepare the cards
        evaluator = treys.Evaluator()
        deck = self.__cards_treys.copy()
        
        hole_cards = [treys.Card.new(f"{card.rank}{card.suit}") for card in hole_cards]
        board_cards = [treys.Card.new(f"{card.rank}{card.suit}") for card in board_cards]

        for card in hole_cards + board_cards:
            deck.remove(card)

        wins = 0

        for _ in range(n_simulations):
            sampled_cards = random.sample(deck, 5 - len(board_cards) + 2 * (n_players - 1))

            # Create a simulated board
            simulated_board = board_cards + sampled_cards[:5 - len(board_cards)]
            my_score = evaluator.evaluate(hand=hole_cards, board=simulated_board)

            # Simulate other players' hands
            best_score = True
            for i in range(n_players - 1):
                start = 5 - len(board_cards) + i * 2
                enemy_hole_cards = sampled_cards[start:start + 2]
                enemy_score = evaluator.evaluate(hand=enemy_hole_cards, board=simulated_board)

                if my_score > enemy_score:
                    best_score = False
                    break

            if best_score:
                wins += 1

        return wins / n_simulations