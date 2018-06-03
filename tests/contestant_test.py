import os
import sys
src_path = os.path.abspath(os.path.join('../src'))
sys.path.append(src_path)
from contestant import Contestant
from unittest import TestCase
import pytest


class ContestantTest(TestCase):

    def setUp(self):
        return

    @pytest.mark.xfail(raises=ImportError)
    def test_import_invalid_name(self):
        invalid_ai_name = "foo"
        Contestant(ai_name=invalid_ai_name)

    # This test relies on the existence of the Machete.py class inside the AIs/ directory
    def test_import_valid_name(self):
        valid_ai_name = 'Machete'
        ct = Contestant(ai_name=valid_ai_name)
        assert ct.ai_name == valid_ai_name

    def test_instantiate_contestant_ai(self):
        valid_ai_name = 'Machete'
        ct = Contestant(ai_name=valid_ai_name)

        ai = ct.instantiate_ai(gateway=None)
        assert ai.__class__.__name__ == valid_ai_name
        assert ai.__class__.__name__ == ct.ai_name

    def test_character_valid(self):
        Contestant(ai_name='Machete', character='ZEN')
        Contestant(ai_name='Machete', character='GARNET')

    @pytest.mark.xfail(raises=ValueError)
    def test_character_invalid(self):
        Contestant(ai_name='Machete', character='CARLOS')

    @pytest.mark.xfail(raises=ValueError)
    def test_finds_all_available_contestant_module_names_non_list_input(self):
        test_ai_module_path = '{}/test_dirs/AIs/'.format(os.getcwd())
        Contestant.available_contestants([test_ai_module_path])

    def test_finds_all_available_contestant_module_names(self):
        test_ai_module_path = '{}/test_dirs/AIs/'.format(os.getcwd())
        expected_contestants = ['AI_1']
        available_contestants = Contestant.available_contestants([test_ai_module_path])
        assert expected_contestants == available_contestants
