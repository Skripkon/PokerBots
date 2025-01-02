import random
from .BasePlayer import BasePlayer


class RandomPlayer(BasePlayer):
    """
    A poker player that selects actions randomly from the set of valid actions.

    This class extends the BasePlayer and implements the `play` method by choosing
    actions randomly. It ensures that the chosen action is valid according to the
    provided valid actions.

    Methods:
        play(valid_actions: dict) -> tuple[str, float]:
            Selects a random action from the set of valid actions and returns it along
            with the corresponding chip amount if applicable.
    """

    def play(self, valid_actions: dict) -> tuple[str, float]:
        """
        Randomly selects an action from the valid actions and determines the bet amount if needed.

        Args:
            valid_actions (dict): A dictionary containing the actions the player can take.
                Format:
                    valid_actions["fold"] = 0 (indicates folding is an option)
                    valid_actions["check"] = 0 (indicates checking is an option)
                    valid_actions["call"] = <amount> (indicates calling is an option with a specified amount)
                    valid_actions["raise"] = {"min": <min_amount>, "max": <max_amount>}
                        (indicates raising is an option with specified minimum and maximum limits)

        Returns:
            tuple[str, float]: A tuple containing the chosen action as a string and the amount of chips
            associated with the action:
                - For "fold" or "check": (action, 0)
                - For "call": (action, valid_actions["call"])
                - For "raise": (action, randomly selected amount between "min" and "max")

        Raises:
            ValueError: If an unexpected action is encountered in the valid_actions dictionary.
        """
        action = random.choice(list(valid_actions.keys()))

        if action in ["fold", "check"]:
            return action, 0

        elif action == "call":
            bet = valid_actions[action]
            return action, bet

        elif action == "raise":
            raise_amount = random.randint(valid_actions["raise"]["min"], 
                                          valid_actions["raise"]["max"])
            return action, raise_amount

        else:
            raise ValueError(f"Unexpected action: {action}")
