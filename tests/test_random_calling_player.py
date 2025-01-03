from PokerBots.game.Game import Game
from PokerBots.players.CallingPlayer import CallingPlayer


def test_game_simulation_with_calling_players():
    game = Game(small_blind=20)
    player1 = CallingPlayer(stack=10_000, name="Igor")
    player2 = CallingPlayer(stack=10_000, name="Ivan")

    game.set_player_1(player=player1)
    game.set_player_2(player=player2)

    for _ in range(100):
        game.play_round()
        if player1.stack == 0 or player2.stack == 0:
            break

def test_100_game_simulations_with_calling_players():
    test_game_simulation_with_calling_players()

