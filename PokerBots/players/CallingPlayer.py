from pokerkit import State
from PokerBots.players.BasePlayer import BasePlayer


class CallingPlayer(BasePlayer):
    """
    A poker player that always calls or checks.
    """

    def play(self, valid_actions: dict[str, float], state: State) -> tuple[str, float]:
        """
        Always chooses the "check_or_call" action.

        Args:
            valid_actions (dict): A dictionary containing valid actions and their corresponding amounts.
            state: The current state of the game (not used).

        Returns:
            tuple[str, float]: A tuple with the action "check_or_call" and its associated amount.
        """
        return "check_or_call", valid_actions["check_or_call"]
