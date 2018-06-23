import os
from .exceptions import InvalidRootPath


def ValidateRootPath(path):
    if not os.path.exists(path):
        raise InvalidRootPath("Root path '%s' does not exist" % path)
    cmakeListsFile = os.path.join(path, 'CMakeLists.txt')
    if not os.path.isfile(cmakeListsFile):
        raise InvalidRootPath("Root path '%s' does not conatin a " \
            "CMakeLists.txt file")