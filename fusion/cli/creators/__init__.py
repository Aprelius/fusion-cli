from .executable import CreateExecutable, SetupExecutableCreator
from .library import CreateLibrary, SetupLibraryCreator


def RunCreator(creator, args):
    if creator == 'executable':
        return CreateExecutable(args)
    if creator == 'library':
        return CreateLibrary(args)
    raise RuntimeError("Unknown creator '%s'" % creator)


def SetupCreator(creator, commands):
    if creator == 'executable':
        return SetupExecutableCreator(commands)
    if creator == 'library':
        return SetupLibraryCreator(commands)
    raise RuntimeError("Unknown creator '%s'" % creator)