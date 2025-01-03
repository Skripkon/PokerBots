from PokerBots.game.Game import Game
from PokerBots.players.RandomPlayer import RandomPlayer


def test_game_simulation_with_random_players():
    game = Game(small_blind=20)
    player1 = RandomPlayer(stack=10_000, name="Igor")
    player2 = RandomPlayer(stack=10_000, name="Ivan")

    game.set_player_1(player=player1)
    game.set_player_2(player=player2)

    for _ in range(100):
        game.play_round()
        if player1.stack == 0 or player2.stack == 0:
            break


def test_100_game_simulations_with_random_players():
    for _ in range(100):
        game = Game(small_blind=20)
        player1 = RandomPlayer(stack=10_000, name="Igor")
        player2 = RandomPlayer(stack=10_000, name="Ivan")

        game.set_player_1(player=player1)
        game.set_player_2(player=player2)

        for _ in range(100):
            game.play_round()
            if player1.stack == 0 or player2.stack == 0:
                break
