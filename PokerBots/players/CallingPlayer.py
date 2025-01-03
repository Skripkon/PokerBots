from PokerBots.players.BasePlayer import BasePlayer


class CallingPlayer(BasePlayer):
    """
    A poker player that calls every time it's possible.
    """

    def play(self, state: dict) -> tuple[str, float]:

        if state["action"]["call"] != -1:
            return "call", state["action"]["call"]
        
        return "fold", 0
