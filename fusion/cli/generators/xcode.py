from .base import BaseProjectGenerator


def SetupXCodeProjectGenerator(commands):
    BaseProjectGenerator(commands, 'xcode',
        help='Generate an XCode project.')


def GenerateXCodeProject(args):
    return False