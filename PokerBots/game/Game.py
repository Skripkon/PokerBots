from pokerkit import Automation, NoLimitTexasHoldem
from PokerBots.players.BasePlayer import BasePlayer 
from PokerBots.players.CallingPlayer import CallingPlayer
from PokerBots.players.RandomPlayer import RandomPlayer

class Game:
    """
    Represents a game of No-Limit Texas Hold'em poker.

    Attributes:
        players (list[BasePlayer]): List of player objects participating in the game.
        n_players (int): Number of players in the game.
        stacks (list[float]): Current stack for each player.
        state (NoLimitTexasHoldem.State): Current game state.
    """

    def __init__ (self, initial_stack: float = 30_000, players: list[BasePlayer] = None):
        """
        Initializes the Game instance with the given players and initial stack (the same for each player).

        Args:
            initial_stack (float): Starting chip count for each player. Default is 30,000.
            players (list[BasePlayer]): List of player objects. Default is [RandomPlayer(), CallingPlayer()].
        """
        if players is None:
            self.players = [RandomPlayer(), CallingPlayer()]
        else:
            self.players = players
        self.n_players = len(players)
        self.stacks = [initial_stack] * self.n_players

        self.state = None

    def play_round(self, verbose: bool = True):
        """
        Plays a single round of No-Limit Texas Hold'em poker.

        Args:
            verbose (bool): If True, logs detailed information about the round. Default is True.

        Returns:
            bool: True if the game is over, otherwise False.
        """
        if verbose:
            print("INFO: ROUND STARTS")
            print(f"INFO: stacks = {self.stacks}")

        # Initialize the game state
        self.state = NoLimitTexasHoldem.create_state(
            (
                Automation.ANTE_POSTING,
                Automation.BET_COLLECTION,
                Automation.BLIND_OR_STRADDLE_POSTING,
                Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
                Automation.HAND_KILLING,
                Automation.CHIPS_PUSHING,
                Automation.CHIPS_PULLING,
            ),
            True,  # Uniform antes
            500,  # Antes
            (1000, 2000),  # Blinds or straddles
            2000,  # Min-bet
            self.stacks,  # Starting stacks
            self.n_players,  # Number of players
        )

        # Deal hole cards and log initial game state
        self.__deal_cards()
        if verbose:
            self.__log_posting_of_blinds_or_straddles()

        # Play the streets (Preflop, Flop, Turn, River)
        for street_name, cards_to_deal in (("PREFLOP", 0), ("FLOP", 3), ("TURN", 1), ("RIVER", 1)):
            if cards_to_deal > 0:
                # Dealing might be impossible if all players except for one folded.
                self.__try_to_burn_and_deal_cards(n_cards=cards_to_deal)

            if self.state.actor_index is not None:
                if verbose:
                    print(f"INFO: ===== {street_name} =====")
                self.__play_street(verbose=verbose)

        # Update stacks and log results
        self.stacks = self.state.stacks
        if verbose:
            self.__log_results()

        # Remove bankrupt players and check if the game is over
        self.__remove_bankrupt_players()
        return self.__check_if_game_is_over(verbose=verbose)


    def __deal_cards(self):
        """
        Deals two hole cards to each player in the game.
        """
        for _ in range(self.state.player_count):
            self.state.deal_hole(2)

    def __play_street(self, verbose: bool = True):
        """
        Manages the betting actions of players for a single betting street.

        Args:
            verbose (bool): Whether to log player actions. Default is True.
        """
        while self.state.actor_index is not None:
            current_player_idx = self.state.actor_index
            valid_actions = self.__get_valid_actions()
            action, amount = self.players[current_player_idx].play(valid_actions=valid_actions, state=self.state)

            match action:
                case "fold":
                    self.state.fold()
                    if verbose:
                        print(f"INFO: Player {self.players[current_player_idx].name} folds.")
                case "check_or_call":
                    self.state.check_or_call()
                    if verbose:
                        if amount == 0:
                            print(f"INFO: Player {self.players[current_player_idx].name} checks.")
                        else:
                            print(f"INFO: Player {self.players[current_player_idx].name} calls {amount}.")
                case "complete_bet_or_raise_to":
                    self.state.complete_bet_or_raise_to(amount=amount)
                    if verbose:
                        print(f"INFO: Player {self.players[current_player_idx].name} raises to {amount}")
                case _:
                    raise ValueError(f"Unknown action: {action}. Valid actions are ['fold', 'check_or_call', 'complete_bet_or_raise_to']")

    def __get_valid_actions(self):
        """
        Determines the valid actions available to the current player.

        Returns:
            dict: A dictionary mapping action names to their respective amounts or ranges.
        """
        valid_actions = {"fold": 0}
        if self.state.can_check_or_call():
            valid_actions["check_or_call"] = self.state.checking_or_calling_amount
        
        if self.state.can_complete_bet_or_raise_to():
            valid_actions["complete_bet_or_raise_to"] = (self.state.min_completion_betting_or_raising_to_amount, self.state.max_completion_betting_or_raising_to_amount)

        return valid_actions

    def __remove_bankrupt_players(self):
        """
        Removes players with zero stack from the game.
        """
        self.stacks, self.players = zip(
            *[(stack, player) for stack, player in zip(self.stacks, self.players) if stack > 0]
        )
        self.stacks = list(self.stacks)
        self.players = list(self.players)
        self.n_players = len(self.players)


    def __check_if_game_is_over(self, verbose: bool = True):
        """
        Checks whether the game is over (only one player remains).

        Args:
            verbose (bool): Whether to log the winner. Default is True.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        if len(self.stacks) == 1:
            if verbose:
                print(f"INFO: Player {self.players[0].name} won the Tournament.")
            return True
        
        return False
    
    def __log_results(self):
        """
        Logs the results of the round, including winnings or losses for each player.
        """
        print("INFO: ===== ROUND RESULTS =====")
        for idx in range(self.n_players):
            payoff = self.state.payoffs[idx]
            if payoff >= 0:
                print(f"INFO: Player {self.players[idx].name} won {payoff}")
            else:
                print(f"INFO: Player {self.players[idx].name} lost {-payoff}")
        print("==========================================")

    def __try_to_burn_and_deal_cards(self, n_cards: int = 1):
        """
        Attempts to burn one card and deal the specified number of community cards.

        Args:
            n_cards (int): Number of community cards to deal. Default is 1.
        """
        if self.state.can_burn_card():
            self.state.burn_card()
            self.state.deal_board(n_cards)

    def __log_posting_of_blinds_or_straddles(self):
        """
        Logs the posting of blinds or straddles at the start of the round.
        """
        for idx, straddle in enumerate(self.state.blinds_or_straddles):
            if straddle > 0:
                print(f"INFO: Player {self.players[idx].name} bets {straddle}.")
