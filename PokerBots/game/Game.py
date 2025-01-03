from treys import Deck, Card, Evaluator
from ..players.BasePlayer import BasePlayer


class Game:
    """
    Represents a poker game simulation with two players, a deck, and game state management.

    Attributes:
        small_blind (float): The value of the small blind bet.
        big_blind (float): The value of the big blind bet (double the small blind).
        max_rounds (int): Maximum number of rounds allowed in the game.
        deck (Deck): The card deck used in the game.
        board (list[Card]): The community cards on the board.
        players (list[BasePlayer]): The two players in the game.
        dealer (int): Index of the current dealer (0 or 1).
        evaluator (Evaluator): Evaluator to assess hand strength.
        state (dict): The current game state, used for tracking progress.
        verbose (bool): If True, logs additional details during gameplay.
    """

    def __init__(self, small_blind: float = 20, verbose: bool = False):
        """
        Initializes the Game object with the specified parameters.

        Args:
            small_blind (float): The value of the small blind bet. Defaults to 20.
            max_rounds (int): Maximum number of rounds allowed in the game. Defaults to 100.
            verbose (bool): If True, enables detailed logging. Defaults to False.
        """
        self.small_blind = small_blind
        self.big_blind = 2 * small_blind

        self.deck: Deck = None
        self.board: list[Card] = []
        self.players: list[BasePlayer] = [None, None]

        self.dealer: int = 0
        self.evaluator = Evaluator()

        self.state: dict = None
        self.verbose = verbose

    def set_player_1(self, player: BasePlayer):
        """Sets the first player (position 0)."""
        self.__set_player(player, 0)

    def set_player_2(self, player: BasePlayer):
        """Sets the second player (position 1)."""
        self.__set_player(player, 1)

    def __set_player(self, player: BasePlayer, position: int):
        """
        Sets a player for the specified position.

        Args:
            player (BasePlayer): The player instance to set.
            position (int): The position to assign the player (0 or 1).
        """
        self.players[position] = player

    def play_round(self):
        def play_stage(stage_name, stage_method):
            """Helper function to play a stage and check if the game should finish."""
            if self.verbose:
                print(f"INFO: {stage_name.upper()}")
            if stage_method() != 0:
                self.__finish_game()
                return False
            return True

        if self.verbose:
            print("INFO: ROUND BEGINS")
        self.__set_up_round()

        stages = [
            ("preflop", self.__play_preflop),
            ("flop", self.__play_flop),
            ("turn", self.__play_turn),
        ]

        for stage_name, stage_method in stages:
            if not play_stage(stage_name, stage_method):
                return None

        if self.verbose:
            print("INFO: RIVER")
        self.__play_river()
        self.__finish_game()
        return None

    def __set_up_round(self):
        if self.dealer == 0:
            self.dealer = 1
        else:
            self.dealer = 0

        self.deck = Deck()
        self.board = []

        for player in self.players:
            player.hole_cards = self.deck.draw(2)
            player.folded = False
            player.pot = 0

    def __determine_valid_actions(self, player: BasePlayer, enemy_bet: float):
        valid_actions = {"fold": -1,
                         "call": -1,
                         "check": -1,
                         "raise": {"min": -1, "max": -1}}

        if enemy_bet > 0:
            valid_actions["fold"] = 0
            valid_actions["call"] = min(player.stack, enemy_bet)
        else:  # enemy_bet == 0
            valid_actions["check"] = 0

        if player.stack > enemy_bet:
            valid_actions["raise"]["min"] = enemy_bet
            valid_actions["raise"]["max"] = player.stack

        return valid_actions

    def __play_street(self):
        while self.players[0].pot != self.players[1].pot and self.players[0].stack > 0 and self.players[1].stack > 0:
            for i in [1 - self.dealer, self.dealer]:
                enemy_pot = self.players[1 - i].pot
                enemy_bet = enemy_pot - self.players[i].pot
                valid_actions = self.__determine_valid_actions(
                    self.players[i], enemy_bet)
                state = {
                    "action": valid_actions,
                    "board": self.board
                }
                action, amount = self.players[i].play(state)

                if action == "fold":
                    self.players[i].folded = True
                    if self.verbose:
                        print(f"INFO: {self.players[i].name} folds.")
                    return 1
                if self.verbose:
                    print(f"INFO: {self.players[i].name} {action}s {amount}")

                self.players[i].pot += amount
                self.players[i].stack -= amount

        return 0

    def __play_preflop(self) -> bool:
        bet1 = min(self.small_blind, self.players[1 - self.dealer].stack)
        self.players[1 - self.dealer].stack -= bet1
        self.players[1 - self.dealer].pot += bet1
        if self.verbose:
            print(f"INFO: {self.players[1 - self.dealer].name} bets {bet1}")

        bet2 = min(self.players[self.dealer].stack, self.big_blind)
        self.players[self.dealer].stack -= bet2
        self.players[self.dealer].pot += bet2
        if self.verbose:
            print(f"INFO: {self.players[self.dealer].name} bets {bet2}")

        return self.__play_street()

    def __play_flop(self):
        self.board.extend(self.deck.draw(3))
        return self.__play_street()

    def __play_turn(self):
        self.board.extend(self.deck.draw(1))
        return self.__play_street()

    def __play_river(self):
        self.board.extend(self.deck.draw(1))
        return self.__play_street()

    def __finish_game(self):
        """
        Finalizes the game by resolving the winner and updating player stacks.
        Handles scenarios for folding, winning by hand strength, or splitting the pot.
        """
        total_pot = self.players[0].pot + self.players[1].pot
        for i in range(2):
            if self.players[i].folded:
                winner = 1 - i
                self.players[winner].stack += total_pot
                if self.verbose:
                    print(f"INFO: {self.players[winner].name} won {total_pot}")
                return

        # Evaluate hand scores
        player_1_hand_score = self.evaluator.evaluate(self.players[0].hole_cards, self.board)
        player_2_hand_score = self.evaluator.evaluate(self.players[1].hole_cards, self.board)

        def resolve_winner(winner, loser):
            """
            Updates the stacks based on the winner and loser pots.
            """
            if self.players[winner].pot < self.players[loser].pot:
                self.players[winner].stack += 2 * self.players[winner].pot
                self.players[loser].stack += self.players[loser].pot - self.players[winner].pot
                won_amount = self.players[winner].pot
            else:
                self.players[winner].stack += self.players[winner].pot + self.players[loser].pot
                won_amount = self.players[loser].pot

            if self.verbose:
                print(f"INFO: {self.players[winner].name} won {won_amount}")

        # Compare hand scores
        if player_1_hand_score > player_2_hand_score:
            resolve_winner(0, 1)
        elif player_1_hand_score < player_2_hand_score:
            resolve_winner(1, 0)
        else:
            # Split the pot in case of a tie
            self.players[0].stack += self.players[0].pot
            self.players[1].stack += self.players[1].pot
            if self.verbose:
                print("INFO: Players split the pool.")
