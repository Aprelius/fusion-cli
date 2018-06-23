__all__ = ['CreateExample', 'SetupExampleCreator']


def SetupExampleCreator(commands):
    command = commands.add_parser('create-example',
        help='Generate a CMake example project and add it to the CMake build ' \
             'pipeline.')
    command.add_argument('example', help='Name of the example to create.')
    return command


def CreateExample(args):
    return False