import random
from pokerkit import State
from PokerBots.players.BasePlayer import BasePlayer

class RandomPlayer(BasePlayer):
    """
    A poker player that makes random valid moves.
    """

    def play(self, valid_actions: dict[str, ], state: State) -> tuple[str, float]:
        """
        Choose a random valid action and amount based on the available actions.
        :param valid_actions: A dictionary with action names as keys and either a single integer
                              or a range (tuple of two integers) as values.
        :param state: The current state of the game (unused here).
        :return: A tuple containing the chosen action and the corresponding amount.
        """
        # Determine the possible actions based on valid_actions.
        possible_actions = ["check_or_call", "fold"]
        if valid_actions.get("complete_bet_or_raise_to"):
            possible_actions.append("complete_bet_or_raise_to")
        
        # Select a random action
        action = random.choice(possible_actions)

        # Determine the amount based on the chosen action.
        # If we choose to fold but can check, then check.
        if action == "fold" and valid_actions["check_or_call"] == 0:
            action = "check_or_call"
            amount = 0
        elif action == "complete_bet_or_raise_to":
            amount = random.randint(*valid_actions[action])
        else:
            amount = valid_actions[action]
        return action, amount
