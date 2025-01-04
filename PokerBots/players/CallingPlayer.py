from PokerBots.players.BasePlayer import BasePlayer

class CallingPlayer(BasePlayer):

    """
    A poker player that calls every time.
    """

    def play(self, valid_actions: dict[str], state) -> tuple[str, float]:
        return "check_or_call", valid_actions["check_or_call"]
