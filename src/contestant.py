import importlib
import hashlib
import pkgutil

valid_characters = ['ZEN', 'GARNET']


class Contestant:

    def __init__(self, ai_name=None, character='ZEN'):
        self.ai_module = importlib.import_module('AIs.{}'.format(ai_name))
        self.ai_name = ai_name
        self.ai = None
        if character not in valid_characters:
            raise ValueError('Character passed as parameter not valid, should be one of {}'.format(valid_characters))
        self.character = character

    def instantiate_ai(self, gateway, match_info=None):
        ai_class = getattr(self.ai_module, self.ai_name)
        return ai_class(gateway, match_info)

    @staticmethod
    def available_contestants(ai_modules_path=['AIs/']):
        '''
        Return a list containing strings of the name of all AIs
        found in the folder found at 'ai_modules_path'
        '''
        if not isinstance(ai_modules_path, (list,)):
            raise ValueError('Input is not a list')
        return [m[1] for m in pkgutil.iter_modules(ai_modules_path)]

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.ai_module == other.ai_module and self.ai_name == other.ai_name
        return False

    def __hash__(self):
        return int(hashlib.md5('{}{}'.format(self.ai_module, self.ai_name).encode()).hexdigest(), 16)
