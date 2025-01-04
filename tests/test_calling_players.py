from PokerBots import Game
from PokerBots import CallingPlayer


def test_game_simulation_with_random_players():
    n_players = 6
    players = [CallingPlayer()] * n_players

    game = Game(players=players, initial_stack=30_000)

    for _ in range(100):
        game_is_over = game.play_round(verbose=False)
        if game_is_over:
            break

def test_100_game_simulations_with_random_players():
    test_game_simulation_with_random_players()