from pokerkit import State

class BasePlayer:
    """
    Represents a base class for a poker player in a game.

    Attributes:
        name (str): The name of the player.

    Methods:
        play(self, valid_actions, state: State) -> tuple[str, float]:
            Determines the player's action based on the current state of the game. This method
            must be implemented by subclasses.
    """

    def __init__(self, name: str = "NPC"):
        self.name = name

    def play(self, valid_actions: dict[str], state: State) -> tuple[str, float]:
        """
        Determines the player's action based on the available valid actions.
        """
        raise NotImplementedError(f"Player {self.__class__.__name__} must implement the 'play' method.")
