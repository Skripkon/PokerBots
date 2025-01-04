<h1 align="center">
<img src="https://github.com/Skripkon/PokerBots/blob/main/PokerBots/images/pokerbots_logo.jpg?raw=true">
</h1><br>

<a href="https://pypi.org/project/PokerBots" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>

### PokerBots is designed for testing bots in Hold'em non limited tournaments.

## 1. Install the library
```bash
$ pip install PokerBots
```

## 2. Explore a simple example
```python

from PokerBots import Game, CallingPlayer


# Define three vanila players
player1 = CallingPlayer(name="Igor")
player2 = CallingPlayer(name="Ivan")
player3 = CallingPlayer(name="Ivan")

game = Game(players=[player1, player2, player3], stack=30_000, n_players=n_players)

# Run 1 round
game.play_round()
```

If you want to see a detailed output during the games, then set ```verbose=True```:

## 3. Create Your Own Bot

Creating new bots is a straightforward process:

- Inherit from the `BasePlayer` class.
- Override the `play` method: it must return an action and the amount of chips to bet, given the state of the game and valid actions.

```python
from PokerBots import BasePlayer

class MyOwnBot(BasePlayer):

    def play(self, valid_actions: dict[str], state) -> tuple[str, float]:
        """
        Implement a strategy to choose an action.
        """
        pass
```

**Now you can use this bot:**

```python

from PokerBots import Game

# Define two vanila players and one of your own
player1 = MyOwnBot(name="Igor")
player2 = CallingBot(name="Ivan")
player3 = CallingBot(name="Ivan")

game = Game(players=[player1, player2, player3], stack=30_000, n_players=n_players)

# Run 1 round
game.play_round()
```