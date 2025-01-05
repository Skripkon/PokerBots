from PokerBots import Game
from PokerBots import CallingPlayer, RandomPlayer, GamblingPlayer


def simulate_game(players, rounds=100, verbose: bool = False):
    """
    Simulates a single poker game with the given players.

    Args:
        players (list): A list of player objects.
        rounds (int): Maximum number of rounds to play in the game.
        verbose (bool): If positive, prints logs.
    """
    # Set up the game with an initial stack for each player
    game = Game(players=players, initial_stack=300_000)

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
    players[0].name, players[1].name, players[2].name = "Calling 1", "Calling 2", "Calling 3"
    return players

def create_random_players():
    """
    Creates a list of RandomPlayer objects with predefined names.

    Returns:
        list: A list of RandomPlayer objects.
    """
    players = [RandomPlayer(), RandomPlayer(), RandomPlayer()]
    players[0].name, players[1].name, players[2].name = "Random 1", "Random 2", "Random 3"
    return players

def create_gambling_players():
    """
    Creates a list of GamblingPlayer objects with predefined names.

    Returns:
        list: A list of GamblingPlayer objects.
    """
    players = [GamblingPlayer(), GamblingPlayer(), GamblingPlayer()]
    players[0].name, players[1].name, players[2].name = "Gamble 1", "Gamble 2", "Gamble 3"
    return players

# Test with calling players
def test_multiple_game_simulations_with_calling_players(num_simulations=10, rounds=20):
    simulate_multiple_games(create_calling_players(), num_simulations, rounds, verbose=True)
    simulate_multiple_games(create_calling_players(), num_simulations, rounds, verbose=False)

# Test with random players
def test_multiple_game_simulations_with_random_players(num_simulations=10, rounds=20):
    simulate_multiple_games(create_random_players(), num_simulations, rounds, verbose=True)
    simulate_multiple_games(create_random_players(), num_simulations, rounds, verbose=False)

# Test with gambling players
def test_multiple_game_simulations_with_gambling_players(num_simulations=10, rounds=100):
    simulate_multiple_games(create_gambling_players(), num_simulations, rounds, verbose=True)
    simulate_multiple_games(create_gambling_players(), num_simulations, rounds, verbose=False)

# Test with all players
def test_multiple_game_simulations_with_different_players(num_simulations=10, rounds=100):
    players = [GamblingPlayer(name="Gambler"), RandomPlayer(name="Random"), CallingPlayer(name="Caller")]
    simulate_multiple_games(players, num_simulations, rounds, verbose=False)
    simulate_multiple_games(players, num_simulations, rounds, verbose=False)
