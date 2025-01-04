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

        Args:
            valid_actions (dict): A dictionary mapping action names to either a single integer
                                  or a range (tuple of two integers) representing the valid amount(s).
            state (State): The current state of the game (not used in this implementation).

        Returns:
            tuple[str, float]: A tuple with the chosen action and the corresponding amount.
        """
        # Define the set of possible actions
        possible_actions = ["check_or_call", "fold"]
        if "complete_bet_or_raise_to" in valid_actions:
            possible_actions.append("complete_bet_or_raise_to")

        # Choose a random action from the available options
        action = random.choice(possible_actions)

        # Determine the amount associated with the chosen action
        if action == "fold" and valid_actions.get("check_or_call") == 0:
            # If folding is chosen but checking is free, switch to "check_or_call"
            action, amount = "check_or_call", 0

        elif action == "complete_bet_or_raise_to":
            # For raising, choose a random amount within the valid range
            amount = random.randint(*valid_actions[action])

        else:
            # Use the predefined amount for other actions
            amount = valid_actions[action]

        return action, amount
