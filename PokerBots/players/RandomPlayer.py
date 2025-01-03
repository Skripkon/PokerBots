import random
from PokerBots.players.BasePlayer import BasePlayer


class RandomPlayer(BasePlayer):
    """
    A poker player that selects actions randomly from the set of valid actions.
    """

    def play(self, state: dict) -> tuple[str, float]:
        """
        Randomly selects an action from the valid actions and determines the bet amount if needed.
        """
        valid_actions = ["fold"]
        for action in ("call", "check"):
            if state["action"][action] != -1:
                valid_actions.append(action)

        if state["action"]["raise"]["max"] != -1:
            valid_actions.append("raise")

        action = random.choice(valid_actions)

        if action in {"fold", "check"}:
            return action, 0

        if action == "call":
            bet = state["action"][action]
            return action, bet

        # Else: action == "raise"
        raise_amount = random.randint(state["action"]["raise"]["min"],
                                      state["action"]["raise"]["max"])
        return action, raise_amount
