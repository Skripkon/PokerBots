# PokerBots

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
player1 = RandomPlayer(stack=10_000, name="Igor")
player2 = RandomPlayer(stack=10_000, name="Ivan")

# Add these players to the table just created
game.set_player_1(player=player1)
game.set_player_2(player=player2)

# Run 100 rounds (or until one of them will go bankrupt)
for r in range(100):
    print("======================================================")
    res = game.play_round()
    print(f"Igor stack: {player1.stack}")
    print(f"Ivan stack: {player2.stack}")

    if player1.stack == 0 or player2.stack == 0:
        break
```

If you want to see a detailed output during the games:

```python
game = Game(small_blind=10, verbose=True)
```

## 3. Create your own bot

```python
from PokerBots import BasePlayer

class NewBot(BasePlayer):

    def play(self, valid_actions: dict) -> tuple[str, float]:
        """
        Randomly selects an action from the valid actions and determines the bet amount if needed.
        """
```