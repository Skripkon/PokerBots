from ..game.Game import Game
from ..players.RandomPlayer import RandomPlayer


if __name__ == "__main__":
    game = Game(small_blind=10)
    player1 = RandomPlayer(stack=10000, name="Igor")
    player2 = RandomPlayer(stack=10000, name="Ivan")

    game.set_player_1(player=player1)
    game.set_player_2(player=player2)

    for r in range(100):
        print("======================================================")
        res = game.play_round()
        print(f"Igor stack: {player1.stack}")
        print(f"Ivan stack: {player2.stack}")

        if player1.stack == 0 or player2.stack == 0:
            break
