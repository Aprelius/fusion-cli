__all__ = ['CreateConcept', 'SetupConceptCreator']


def SetupConceptCreator(commands):
    command = commands.add_parser('create-concept',
        help='Generate a CMake concept project and add it to the CMake build '\
             'pipeline.')
    command.add_argument('concept', help='Name of the concept to create.')
    return command


def CreateConcept(args):
    return False
