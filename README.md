<h1 align="center">
<img src="https://github.com/Skripkon/PokerBots/blob/main/PokerBots/images/pokerbots_logo.jpg?raw=true">
</h1><br>

<div style="display: flex; align-items: center; gap: 30px;">
    <a href="https://pypi.org/project/PokerBots/" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/pokerkit" height="30" alt="Supported Python versions">
    </a>
    <a href="https://pepy.tech/projects/pokerbots" target="_blank">
        <img src="https://static.pepy.tech/badge/pokerbots" height="30" alt="PyPI Downloads">
    </a>
    <a href="https://github.com/Skripkon/PokerBots/blob/main/LICENSE" target="_blank">
        <img src="https://raw.githubusercontent.com/Skripkon/PokerBots/27bba4cc02db1a785a9c6623f807f7e138ebbbf7/PokerBots/images/MIT_license.svg" height="30" alt="MIT License">
    </a>
    <a href="https://pypi.org/project/PokerBots/" target="_blank">
        <img src="https://raw.githubusercontent.com/Skripkon/PokerBots/0cd3625896bcd55100b42af3df5d8288f9c446a4/PokerBots/images/coverage.svg" height="30" alt="MIT License">
    </a>
</div>

# Test your bots in no-limit hold'em tournaments!

## 1. Install the library
```bash
$ pip install PokerBots
```

## 2. Explore a simple example
```python

from PokerBots import Game, CallingPlayer, RandomPlayer, GamblingPlayer

# Define three vanila players
player1 = GamblingPlayer(name="Igor")
player2 = CallingPlayer(name="Ivan")
player3 = RandomPlayer(name="Maria")

game = Game(players=[player1, player2, player3], initial_stack=30_000)

# See current stacks:
print(game.stacks)  # [30_000, 30_000, 30_000]

# Run 1 round
game.play_round(verbose=False)

# See stacks after one round:
print(game.stacks)  # [27500, 35000, 27500]
```

> [!TIP]
> If you want to see a detailed output during the games, then set ```verbose=True```.

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
state.hole_cards[state.actor_index]
```

### All official bots can be found in ```PokerBots/players/```