__all__ = ['CreateLibrary', 'SetupLibraryCreator']

def SetupLibraryCreator(commands):
    command = commands.add_parser('create-library',
        help='Generate a CMake library project and add it to the CMake build ' \
            'pipeline.')
    command.add_argument('--protocol', '-p', action='store_true', default=False,
        help='Build the library as a protocol, not a library. This will add ' \
             'the generated files to the procols folder, not the libraries ' \
             'folder.')
    command.add_argument('library', help='Name of the library to create')
    return command


def CreateLibrary(args):
    return False
