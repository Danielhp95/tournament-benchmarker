import os
import sys
src_path = os.path.abspath(os.path.join('../src'))
sys.path.append(src_path)
from contestant import Contestant
from tournament import Tournament
from tournament import TournamentType
from tournament import Match as Match
from unittest import TestCase
import pytest


class TournamentTest(TestCase):
    '''
        BIG NOTE: this test class is heavily reliant on the existence of a directory
        whose relative  path is '../../AIs/. It also relies on such directory having
        and on that folder having the following AIs: Machete, RandomAI, KickAI
    '''

    @pytest.mark.xfail(raises=ValueError)
    def test_tournament_creation_invalid_tournament_type(self):
        Tournament(tournament_type=None)

    def test_tournament_creation_tournament_type(self):
        Tournament(tournament_type=TournamentType.FLAT_KNOCKOUT, contestant_names=['Machete'])
        Tournament(tournament_type=TournamentType.ROUND_KNOCKOUT, contestant_names=['Machete'])
        Tournament(tournament_type=TournamentType.ROUND_ROBIN, contestant_names=['Machete'], round_robin_rounds=1)

    def test_check_initialization_statistics(self):
        tournament = Tournament(tournament_type=TournamentType.ROUND_ROBIN, contestant_names=['Machete', 'RandomAI'], round_robin_rounds=1)

        # TODO  check if this test needs to be changed
        assert tournament.matches == 0
        assert tournament.total_duration == 0
        assert tournament.average_duration == 0
        assert tournament.has_tournament_started == False
        assert tournament.is_tournament_over == False

    @pytest.mark.xfail(raises=ValueError)
    def test_empty_contestant_non_list(self):
        Tournament(tournament_type=TournamentType.ROUND_ROBIN, contestant_names='Daniiii', round_robin_rounds=1)

    @pytest.mark.xfail(raises=ValueError)
    def test_empty_contestant_list(self):
        Tournament(tournament_type=TournamentType.ROUND_ROBIN, contestant_names=[], round_robin_rounds=1)

    def test_create_matches_round_robin_single_round(self):
        t = Tournament(tournament_type=TournamentType.ROUND_ROBIN, round_robin_rounds=1, contestant_names=['Machete', 'RandomAI'])
        expected_matches = [Match(Contestant('Machete'), Contestant('RandomAI'), winner=None, duration=-1)]
        actual_matches, selected_round_winners = t.calculate_round_matches(t.contestants)
        assert selected_round_winners == []
        assert len(expected_matches) == len(actual_matches)
        assert actual_matches[0].contestant_1 == expected_matches[0].contestant_1
        assert actual_matches[0].contestant_2 == expected_matches[0].contestant_2

    def test_create_matches_round_robin_multiple_rounds(self):
        t = Tournament(tournament_type=TournamentType.ROUND_ROBIN, round_robin_rounds=2, contestant_names=['Machete', 'RandomAI'])
        expected_matches = [Match(Contestant('Machete'), Contestant('RandomAI'), winner=None, duration=-1)] * 2
        actual_matches, selected_round_winners = t.calculate_round_matches(t.contestants)
        assert selected_round_winners == []
        assert len(expected_matches) == len(actual_matches)
        assert all([actual_matches[i].contestant_1 == expected_matches[i].contestant_1 for i in range(len(actual_matches))])
        assert all([actual_matches[i].contestant_2 == expected_matches[i].contestant_2 for i in range(len(actual_matches))])

    def test_create_matches_round_knockout(self):
        t = Tournament(tournament_type=TournamentType.ROUND_KNOCKOUT, round_robin_rounds=2, contestant_names=['Machete', 'RandomAI'])
        actual_matches, selected_round_winners = t.calculate_round_matches(t.contestants)
        expected_matches_1 = [Match(Contestant('Machete'), Contestant('RandomAI'), winner=None, duration=-1)]
        expected_matches_2 = [Match(Contestant('RandomAI'), Contestant('Machete'), winner=None, duration=-1)]
        assert selected_round_winners == []
        assert len(expected_matches_1) == len(actual_matches)
        permutation_1_comparison_1 = actual_matches[0].contestant_1 == expected_matches_1[0].contestant_1
        permutation_1_comparison_2 = actual_matches[0].contestant_2 == expected_matches_1[0].contestant_2
        permutation_2_comparison_1 = actual_matches[0].contestant_2 == expected_matches_2[0].contestant_2
        permutation_2_comparison_2 = actual_matches[0].contestant_2 == expected_matches_2[0].contestant_2
        assert any([all([permutation_1_comparison_1, permutation_1_comparison_2]),
                    all([permutation_2_comparison_1, permutation_2_comparison_2])])

    def test_create_matches_round_knockout_odd_contestants(self):
        t = Tournament(tournament_type=TournamentType.ROUND_KNOCKOUT, round_robin_rounds=2, contestant_names=['Machete', 'RandomAI', 'KickAI'])
        actual_matches, selected_round_winners = t.calculate_round_matches(t.contestants)
        assert len(actual_matches) == 1
        assert len(selected_round_winners) == 1

