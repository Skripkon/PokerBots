from treys import Card


class BasePlayer:
    """
    Represents a base class for a poker player in a game.

    Attributes:
        stack (float): The total amount of chips the player has.
        hole_cards (list[Card]): The player's private cards, also known as hole cards.
        folded (bool): A flag indicating whether the player has folded.
        pot (float): The amount of chips the player has contributed to the pot in the current hand.
        name (str): The name of the player.

    Methods:
        play(valid_actions: dict) -> tuple[str, float]:
            Determines the player's action based on the available valid actions. This method
            must be implemented by subclasses.
    """

    def __init__(self, stack: float, name: str):
        """
        Initializes a BasePlayer instance.

        Args:
            stack (float): The initial stack of chips the player has.
            name (str): The name of the player.
        """
        self.stack: float = stack
        self.hole_cards: list[Card] = []
        self.folded: bool = False
        self.pot: float = 0.0
        self.name: str = name

    def play(self, valid_actions: dict) -> tuple[str, float]:
        """
        Determines the player's action based on the available valid actions.

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
            associated with the action (if applicable).

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError(f"Player {self.__class__.__name__} must implement the 'play' method.")
