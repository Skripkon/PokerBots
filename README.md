<h1 align="center">
<img src="https://github.com/Skripkon/PokerBots/blob/main/PokerBots/images/pokerbots_logo.jpg?raw=true">
</h1><br>

<a href="https://pypi.org/project/PokerBots" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>

# Test you bots in no-limit hold'em tournaments!

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
player3 = CallingPlayer(name="Maria")

game = Game(players=[player1, player2, player3], initial_stack=30_000)

# See current stacks:
print(game.state.stacks)  # [30_000, 30_000, 30_000]

# Run 1 round
game.play_round(verbose=False)

# See stacks after one round:
print(game.state.stacks)  # [27500, 35000, 27500]
```

> [!TIP]
> If you want to see a detailed output during the games, then set ```verbose=True```:

## 3. Create Your Own Bot

Creating new bots is a straightforward process:

- Inherit from the `BasePlayer` class.
- Override the `play` method: it must return an action and the amount of chips to bet, given the state of the game and valid actions.

```python
from PokerBots import BasePlayer
from pokerkit import State

class MyOwnBot(BasePlayer):

    def play(self, valid_actions: dict, state: State) -> tuple[str, float]:
        """
        Implement a strategy to choose an action.
        """
        pass
```

> [!NOTE]  
> ```valid_actions``` is a dictionary. Keys represent valid actions, and values represent the valid amount of chips. If all actions are valid, it will look like this:

```python
valid_actions["fold"] = 0
valid_actions["check_or_call"] = 1_000
valid_actions["complete_bet_or_raise_to"] = (1_000, 50_000)
```

> [!IMPORTANT]
> ```valid_actions["complete_bet_or_raise_to"]``` is a tuple of two numbers: the minimum and maximum raises.

Other information can be obtained from the ```state``` parameter.

For instance, the cards on the board can be accessed as follows:

```python
state.board_cards
```

Or, the player's hole cards:

```python
state.hole_cards
```

### All official bots can be found in ```PokerBots/players/```