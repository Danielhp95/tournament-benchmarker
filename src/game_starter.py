import sys
import os
from contestant import Contestant
ais_path = os.path.abspath(os.path.join('../..'))
sys.path.append(ais_path)

from py4j.java_gateway import JavaGateway, GatewayParameters, CallbackServerParameters


def start_game(contestant_1, contestant_2, gateway, manager, number_of_games):
    p1 = contestant_1.instantiate_ai(gateway)
    p2 = contestant_2.instantiate_ai(gateway)

    manager.registerAI(p1.__class__.__name__, p1)
    manager.registerAI(p2.__class__.__name__, p2)
    print("Starting game: {} VS {}".format(contestant_1.ai_name, contestant_2.ai_name))

    game = manager.createGame("ZEN", "ZEN",
                              contestant_1.ai_name,
                              contestant_2.ai_name,
                              number_of_games)

    manager.runGame(game)

    print("Game finished")
    sys.stdout.flush()
    winner = None
    duration = None
    return winner, duration


def open_gateway(port):
    return JavaGateway(gateway_parameters=GatewayParameters(port=port), callback_server_parameters=CallbackServerParameters())


def close_gateway(gateway):
    gateway.close_callback_server()
    gateway.close()


def play_game(contestant_1, contestant_2, number_of_games=1, port=4242):
    gateway = open_gateway(port)
    manager = gateway.entry_point
    winner, duration = start_game(contestant_1, contestant_2, gateway, manager, number_of_games)
    close_gateway(gateway)
    return winner, duration


winner, duration = play_game(Contestant("KickAI"), Contestant("Machete"))
