import sys
import os
from recordclass import recordclass
from contestant import Contestant
ais_path = os.path.abspath(os.path.join('../..'))
sys.path.append(ais_path)

from py4j.java_gateway import JavaGateway, GatewayParameters, CallbackServerParameters

MatchInformation = recordclass('MatchInformation', 'p1_hp p2_hp duration winner')


def start_game(contestant_1, contestant_2, gateway, manager, number_of_games):
    # We pass the match information to all AIs, even though the will be overriding eachother's information
    match_info = MatchInformation(-1, -1, -1, None)
    p1 = contestant_1.instantiate_ai(gateway, match_info)
    p2 = contestant_2.instantiate_ai(gateway, match_info)

    manager.registerAI(p1.__class__.__name__, p1)
    manager.registerAI(p2.__class__.__name__, p2)
    print("Starting game: {} VS {}".format(contestant_1.ai_name, contestant_2.ai_name))

    game = manager.createGame(contestant_1.character, contestant_2.character,
                              contestant_1.ai_name,
                              contestant_2.ai_name,
                              number_of_games)

    manager.runGame(game)
    print("Game finished")

    sys.stdout.flush()

    # Because both AIs are updating the same variable, we halve its value
    match_info.duration /= 2
    health_array = [match_info.p1_hp, match_info.p2_hp]
    winner_index = health_array.index(max(health_array))
    if winner_index == 0:
        match_info.winner = contestant_1
    else:
        match_info.winner = contestant_2
    return match_info


def open_gateway(port):
    return JavaGateway(gateway_parameters=GatewayParameters(port=port), callback_server_parameters=CallbackServerParameters())


def close_gateway(gateway):
    gateway.close_callback_server()
    gateway.close()
    pass


def play_match(contestant_1, contestant_2, number_of_games=1, port=4242):
    gateway = open_gateway(port)
    manager = gateway.entry_point
    match_info = start_game(contestant_1, contestant_2, gateway, manager, number_of_games)
    close_gateway(gateway)
    return match_info.winner, match_info.duration
