from .concept import CreateConcept, SetupConceptCreator
from .example import CreateExample, SetupExampleCreator
from .library import CreateLibrary, SetupLibraryCreator


def RunCreator(creator, args):
    if creator == 'concept':
        return CreateConcept(args)
    if creator == 'example':
        return CreateExample(args)
    if creator == 'library':
        return CreateLibrary(args)
    raise RuntimeError("Unknown creator '%s'" % creator)


def SetupCreator(creator, commands):
    if creator == 'concept':
        return SetupConceptCreator(commands)
    if creator == 'example':
        return SetupExampleCreator(commands)
    if creator == 'library':
        return SetupLibraryCreator(commands)
    raise RuntimeError("Unknown creator '%s'" % creator)