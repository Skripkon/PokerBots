from pokerkit import Automation, NoLimitTexasHoldem
from PokerBots.players.BasePlayer import BasePlayer 

class Game:

    def __init__ (self, initial_stack: float = 30_000, players: list[BasePlayer] = None):
        self.players = players
        self.n_players = len(players)
        self.stacks = [initial_stack] * self.n_players

        self.state = None

    def play_round(self, verbose: bool = True):
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
            True,  # Uniform antes?
            500,  # Antes
            (1000, 2000),  # Blinds or straddles
            2000,  # Min-bet
            self.stacks,  # Starting stacks
            self.n_players,  # Number of players
        )

        self.__deal_cards()

        # Preflop
        self.__play_street(verbose=verbose)

        # Flop
        self.__try_to_burn_and_deal_cards(n_cards=3)

        if self.state.actor_index is not None:
            self.__play_street(verbose=verbose)

            # Tern
            self.__try_to_burn_and_deal_cards(n_cards=1)
            if self.state.actor_index is not None:
                self.__play_street(verbose=verbose)

                # River
                self.__try_to_burn_and_deal_cards(n_cards=1)
                if self.state.actor_index is not None:
                    self.__play_street(verbose=verbose)
            else:
                # River
                self.__try_to_burn_and_deal_cards(n_cards=1)
        else:
            # Tern
            self.__try_to_burn_and_deal_cards(n_cards=1)
            # River
            self.__try_to_burn_and_deal_cards(n_cards=1)

        # Update stacks
        self.stacks = self.state.stacks

        # Remove players with zero stack
        self.__remove_bankrupt_players(verbose=verbose)

        if verbose:
            self.__log_winner()

        # Check if Game is over
        game_is_over: bool = self.__check_if_game_is_over(verbose=verbose)
        return game_is_over

    def __deal_cards(self):
        """ Deals the hole cards for all players. """
        for _ in range(self.state.player_count):
            self.state.deal_hole(2)

    def __play_street(self, verbose: bool = True):
        while self.state.actor_index is not None:
            current_player_idx = self.state.actor_index
            valid_actions = self.__get_valid_actions()
            action, amount = self.players[current_player_idx].play(valid_actions=valid_actions, state=self.state)

            if verbose:
                match action:
                    case "fold":
                        self.state.fold()
                        print(f"INFO: Player {self.players[current_player_idx].name} folds.")
                    case "check_or_call":
                        self.state.check_or_call()
                        print(f"INFO: Player {self.players[current_player_idx].name} checks/calls.")
                    case "complete_bet_or_raise_to":
                        self.state.complete_bet_or_raise_to(amount=amount)
                        print(f"INFO: Player {self.players[current_player_idx].name} raises to {amount}")
                    case _:
                        raise ValueError(f"Unknown action: {action}. Valid actions are ['fold', 'check_or_call', 'complete_bet_or_raise_to']")
            else:
                match action:
                    case "fold":
                        self.state.fold()
                    case "check_or_call":
                        self.state.check_or_call()
                    case "complete_bet_or_raise_to":
                        self.state.complete_bet_or_raise_to(amount=amount)
                    case _:
                        raise ValueError(f"Unknown action: {action}. Valid actions are ['fold', 'check_or_call', 'complete_bet_or_raise_to']")

    def __get_valid_actions(self):
        valid_actions = {"fold": 0}
        if self.state.can_check_or_call():
            valid_actions["check_or_call"] = self.state.checking_or_calling_amount
        
        if self.state.can_complete_bet_or_raise_to():
            valid_actions["complete_bet_or_raise_to"] = (self.state.min_completion_betting_or_raising_to_amount, self.state.max_completion_betting_or_raising_to_amount)

        return valid_actions

    def __remove_bankrupt_players(self, verbose: bool = True):
        if verbose:
            for idx, stack in enumerate(self.stacks):
                if stack == 0:
                    print(f"INFO: Player {self.players[idx].name} lost his stack.")
        
        self.stacks, self.players = zip(
            *[(stack, player) for stack, player in zip(self.stacks, self.players) if stack > 0]
        )
        self.stacks = list(self.stacks)
        self.players = list(self.players)
        self.n_players = len(self.players)


    def __check_if_game_is_over(self, verbose: bool = True):
        if len(self.stacks) == 1:
            if verbose:
                print(f"INFO: Player {self.players[0].name} won the Tournament.")
            return True
        
        return False
    
    def __log_winner(self):
        for idx in range(self.n_players):
            if self.state.can_win_now(idx):
                print(f"INFO: Player {self.players[idx].name} won.")

    def __try_to_burn_and_deal_cards(self, n_cards: int = 1):
        if self.state.can_burn_card():
            self.state.burn_card()
            self.state.deal_board(n_cards)
