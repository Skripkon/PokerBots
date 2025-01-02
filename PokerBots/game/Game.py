from treys import Deck, Card, Evaluator
from ..players.BasePlayer import BasePlayer


class Game:

    def __init__(self, small_blind: float = 20, max_rounds: int = 100, verbose: bool = False):
        self.small_blind = small_blind
        self.big_blind = 2 * small_blind
        self.max_rounds = max_rounds

        self.deck: Deck = None
        self.board: list[Card] = []
        self.players: list[BasePlayer] = [None, None]

        self.dealer: int = 0
        self.evaluator = Evaluator()

        self.state: dict = None
        self.verbose = verbose

    def set_player_1(self, player: BasePlayer):
        self.players[0] = player

    def set_player_2(self, player: BasePlayer):
        self.players[1] = player

    def play_round(self):
        if self.verbose:
            print("INFO: ROUND BEGINS")
        self.__set_up_round()

        if self.verbose:
            print("INFO: PREFLOP")
        if self.__play_preflop() != 0:
            self.__finish_game()
            return None

        if self.verbose:
            print("INFO: FLOP")
        if self.__play_flop() != 0:
            self.__finish_game()
            return None

        if self.verbose:
            print("INFO: TURN")
        if self.__play_turn() != 0:
            self.__finish_game()
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
        valid_actions = {}
        if player.folded or player.stack <= 0:
            return valid_actions

        if enemy_bet > 0:
            valid_actions["fold"] = 0
            valid_actions["call"] = min(player.stack, enemy_bet)
        else:  # enemy_bet == 0
            valid_actions["check"] = 0

        if player.stack > enemy_bet:
            valid_actions["raise"] = {"min": enemy_bet,
                                      "max": player.stack}

        return valid_actions

    def __play_street(self):
        while self.players[0].pot != self.players[1].pot and self.players[0].stack > 0 and self.players[1].stack > 0:
            for i in [1 - self.dealer, self.dealer]:
                enemy_pot = self.players[1 - i].pot
                enemy_bet = enemy_pot - self.players[i].pot
                valid_actions = self.__determine_valid_actions(
                    self.players[i], enemy_bet)
                action, amount = self.players[i].play(valid_actions)

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
        if self.players[0].folded:
            self.players[1].stack += self.players[0].pot + self.players[1].pot
            if self.verbose:
                print(f"INFO: {self.players[1].name} won {self.players[0].pot}")
            return None

        if self.players[1].folded:
            self.players[0].stack += self.players[0].pot + self.players[1].pot
            if self.verbose:
                print(f"INFO: {self.players[0].name} won {self.players[1].pot}")
            return None

        player_1_hand_score = self.evaluator.evaluate(
            self.players[0].hole_cards, self.board)
        player_2_hand_score = self.evaluator.evaluate(
            self.players[1].hole_cards, self.board)

        if player_1_hand_score > player_2_hand_score:
            if self.players[0].pot < self.players[1].pot:
                self.players[0].stack += 2 * self.players[0].pot
                self.players[1].stack += self.players[1].pot - \
                    self.players[0].pot
                if self.verbose:
                    print(
                        f"INFO: {self.players[0].name} won {self.players[0].pot}")
            else:
                self.players[0].stack += self.players[0].pot + \
                    self.players[1].pot
                if self.verbose:
                    print(
                        f"INFO: {self.players[0].name} won {self.players[1].pot}")

        elif player_1_hand_score < player_2_hand_score:
            if self.players[1].pot < self.players[0].pot:
                self.players[1].stack += 2 * self.players[1].pot
                self.players[0].stack += self.players[0].pot - \
                    self.players[1].pot
                if self.verbose:
                    print(
                        f"INFO: {self.players[1].name} won {self.players[1].pot}")
            else:
                self.players[1].stack += self.players[0].pot + \
                    self.players[1].pot
                if self.verbose:
                    print(
                        f"INFO: {self.players[1].name} won {self.players[0].pot}")
        else:
            self.players[0].stack += self.players[0].pot
            self.players[1].stack += self.players[1].pot
            if self.verbose:
                print("INFO: Players split the pool.")
