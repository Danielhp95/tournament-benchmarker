from enum import Enum
from tqdm import tqdm
from recordclass import recordclass
from collections import namedtuple
import random

import game_starter
from contestant import Contestant


class TournamentType(Enum):
    ROUND_ROBIN = 1
    ROUND_KNOCKOUT = 2
    FLAT_KNOCKOUT = 3


Match = recordclass('Match', 'contestant_1 contestant_2 winner duration')
ContestantStatistics = namedtuple('ContestantStatistics', 'wins played_matches')


# TODO refactor this class into three different classes
class Tournament(object):

    def __init__(self, tournament_type=None, contestant_names=[], round_robin_rounds=None):
        self.check_input(tournament_type, contestant_names, round_robin_rounds)

        self.tournament_type = tournament_type
        self.contestants = [Contestant(name) for name in contestant_names]

        self.initialize_common_statistics()
        self.initialize_type_specific_statistics(round_robin_rounds)

    def initialize_common_statistics(self):
        self.contestant_statistics = {}
        self.leaderboard = []
        self.matches = 0
        self.total_duration = 0
        self.average_duration = 0

        self.is_tournament_over     = False
        self.has_tournament_started = False

    # Maybe it'll become useful in the future
    def initialize_type_specific_statistics(self, round_robin_rounds):
        if self.tournament_type == TournamentType.FLAT_KNOCKOUT:
            pass
        elif self.tournament_type == TournamentType.ROUND_KNOCKOUT:
            pass
        elif self.tournament_type == TournamentType.ROUND_ROBIN:
            self.round_robin_rounds = round_robin_rounds

    def begin_tournament(self):
        self.contestant_statistics = {contestant: ContestantStatistics(0, 0) for contestant in self.contestants}
        if self.tournament_type == TournamentType.FLAT_KNOCKOUT:
            pass
        if self.tournament_type == TournamentType.ROUND_KNOCKOUT:
            pass
        if self.tournament_type == TournamentType.ROUND_ROBIN:
            self.play_round_robin_tournament()

    def calculate_round_matches(self, round_contestants):
        # maybe find other place to put definition of Match?
        selected_round_winners, matches = [], []
        if self.tournament_type == TournamentType.ROUND_ROBIN:
            for i, contestant in enumerate(round_contestants):
                for other_contestant in round_contestants[(i+1):]:
                    matches.append(Match(contestant, other_contestant, None, -1))
            return matches * self.round_robin_rounds, selected_round_winners
        if self.tournament_type == TournamentType.FLAT_KNOCKOUT:
            pass
        if self.tournament_type == TournamentType.ROUND_KNOCKOUT:
            random.shuffle(round_contestants)
            if len(round_contestants) % 2 != 0:
                selected_round_winners = [round_contestants.pop()]

            matches = [Match(round_contestants[i], round_contestants[-(i+1)], None, -1) for i in range(int(len(round_contestants)/2))]
            return matches, selected_round_winners

    def play_round_robin_tournament(self):
        self.has_tournament_started = True
        matches, selected_round_winners = self.calculate_round_matches(self.contestants)
        assert selected_round_winners == []
        for match in tqdm(matches):
            self.play_match(match)
            self.update_statistics_after_match(self.contestant_statistics, match)
        self.average_duration = (self.total_duration) / len(matches)
        assert self.matches == len(matches)
        assert self.total_duration == sum(map(lambda match: match.duration, matches))
        self.is_tournament_over = True

    def play_round_knockout_tournament(self):
        pass

    def play_match(match):
        '''
            Delegates the "playing" of the match to a relevant game_starter.
            Match information is updated from the results of the match
        '''
        winner, duration = game_starter.play_match(match.contestant_1, match.contestant_2)
        match.winner = winner
        match.duration = duration

    def update_statistics_after_match(self, contestant_statistics, match):
        self.matches += 1
        self.total_duration += match.duration

        contestant_statistics[match.contestant_1].wins += 1 if match.winner == match.contestant_1 else 0
        contestant_statistics[match.contestant_1].played_matches += 1
        contestant_statistics[match.contestant_1].played_time += 1

        contestant_statistics[match.contestant_2].wins += 1 if match.winner == match.contestant_2 else 0
        contestant_statistics[match.contestant_2].played_matches += 1
        contestant_statistics[match.contestant_2].played_time += match.duration

    def check_input(self, tournament_type, contestant_names, round_robin_rounds):
        if not isinstance(tournament_type, (TournamentType,)):
            all_tournament_types = list(map(lambda e: str(e.name), TournamentType))
            raise ValueError('Tournament type needs to be: {}'.format(all_tournament_types))
        if not isinstance(contestant_names, (list,)):
            raise ValueError('Contestant needs to be a list')
        if len(contestant_names) <= 0:
            raise ValueError('Contestant list was empty')
        if tournament_type == TournamentType.ROUND_ROBIN:
            if not isinstance(round_robin_rounds, (int,)) or round_robin_rounds <= 0:
                raise ValueError('Round robin rounds must be a positive number')
