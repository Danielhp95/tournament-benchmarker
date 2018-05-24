import importlib
import pkgutil


class Contestant:

    def __init__(self, ai_name=None):
        self.ai_module = importlib.import_module('AIs.{}'.format(ai_name))
        self.ai_name = ai_name

    def instantiate_ai(self, gateway):
        ai_class = getattr(self.ai_module, self.ai_name)
        self.ai = ai_class(gateway)

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
