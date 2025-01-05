from PokerBots import Game
from PokerBots import CallingPlayer, RandomPlayer


def simulate_game(players, rounds=100, verbose: bool = False):
    """
    Simulates a single poker game with the given players.

    Args:
        players (list): A list of player objects.
        rounds (int): Maximum number of rounds to play in the game.
        verbose (bool): If positive, prints logs.
    """
    # Set up the game with an initial stack for each player
    game = Game(players=players, initial_stack=50_000)

    # Play up to the specified number of rounds
    for _ in range(rounds):
        if game.play_round(verbose=verbose):
            break


def simulate_multiple_games(players, num_simulations=100, rounds=100, verbose: bool = False):
    """
    Simulates multiple poker games with the given players.

    Args:
        players (list): A list of player objects.
        num_simulations (int): Number of games to simulate.
        rounds (int): Maximum number of rounds to play in each game.
        verbose (bool): If positive, prints logs.
    """
    for _ in range(num_simulations):
        simulate_game(players, rounds, verbose=verbose)


def create_calling_players():
    """
    Creates a list of CallingPlayer objects with predefined names.

    Returns:
        list: A list of CallingPlayer objects.
    """
    players = [CallingPlayer(), CallingPlayer(), CallingPlayer()]
    players[0].name, players[1].name, players[2].name = "Ivan", "Daniel", "Andrew"
    return players


def create_random_players():
    """
    Creates a list of RandomPlayer objects with predefined names.

    Returns:
        list: A list of RandomPlayer objects.
    """
    players = [RandomPlayer(), RandomPlayer(), RandomPlayer()]
    players[0].name, players[1].name, players[2].name = "Ivan", "Daniel", "Andrew"
    return players


# Test with calling players
def test_multiple_game_simulations_with_calling_players(num_simulations=100, rounds=10):
    simulate_multiple_games(create_calling_players(), num_simulations, rounds, verbose=True)
    simulate_multiple_games(create_calling_players(), num_simulations, rounds, verbose=False)


# Test with random players
def test_multiple_game_simulations_with_random_players(num_simulations=100, rounds=10):
    simulate_multiple_games(create_random_players(), num_simulations, rounds, verbose=True)
    simulate_multiple_games(create_random_players(), num_simulations, rounds, verbose=False)
