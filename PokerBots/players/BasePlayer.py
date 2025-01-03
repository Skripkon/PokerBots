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
        play(state: dict) -> tuple[str, float]:
            Determines the player's action based on the current state of the game. This method
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

    def play(self, state: dict) -> tuple[str, float]:
        """
        Determines the player's action based on the available valid actions.

        Args:
            state (dict): A dictionary containing the actions the player can take.
                Format (-1 indicates that the move is invalid):
                    state = {
                        "action":
                            {
                                "fold":  -1,
                                "call":  -1,
                                "check": -1,
                                "raise":
                                        {
                                            "min": -1,
                                            "max": -1
                                        }
                            }
                        "board": list[Card]
                    }
        Returns:
            tuple[str, float]: A tuple containing the chosen action as a string and the amount of chips
            associated with the action.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError(f"Player {self.__class__.__name__} must implement the 'play' method.")
