<h1 align="center">
<img src="https://github.com/Skripkon/PokerBots/blob/main/PokerBots/images/pokerbots_logo.jpg?raw=true">
</h1><br>

<a href="https://pypi.org/project/PokerBots" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>

### PokerBots is designed for testing bots in Heads-Up Poker (1-vs-1 tournaments)

## 1. Install the library
```bash
$ pip install PokerBots
```

## 2. Explore a simple example
```python

from PokerBots import Game, RandomPlayer

# Create a new table
game = Game(small_blind=10)

# Create two random players
player1 = RandomPlayer(stack=5_000, name="Igor")
player2 = RandomPlayer(stack=10_000, name="Ivan")

# Add these players to the table just created
game.set_player_1(player=player1)
game.set_player_2(player=player2)

# Run 1 round
game.play_round()
```

If you want to see a detailed output during the games, then set ```verbose=True```:

```python
game = Game(small_blind=10, verbose=True)
```

## 3. Create Your Own Bot

Creating new bots is a straightforward process:

- Inherit from the `BasePlayer` class.
- Override the `play` method: it must return an action and the amount of chips to bet, given the state of the game.

```python
from PokerBots import BasePlayer

class NewBot(BasePlayer):

    def play(self, state: dict) -> tuple[str, float]:
        """
        Implement a strategy to choose an action.
        """
        pass
```

> [!IMPORTANT]
> ```state``` has the following format:

```
    state = {
        "action":
            {
                "fold":   0,
                "call":  20,
                "check": -1,
                "raise":
                        {
                            "min": 20,
                            "max": 100
                        }
            }
        "board": list[Card]
    }
```

> [!NOTE]
> Value **-1** indicates that the action is invalid. Otherwise, it's an amount of chips. Fold is always valid.

**Now you can use this bot:**

```python

from PokerBots import Game, RandomPlayer

# Create a new table
game = Game(small_blind=10)

# Create two random players
random_bot = RandomPlayer(stack=5_000, name="Igor")
my_bot = NewBot(stack=10_000, name="Ivan")

# Add these players to the table just created
game.set_player_1(player=random_bot)
game.set_player_2(player=my_bot)

# Run 1 round
game.play_round()
```