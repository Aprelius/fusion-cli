import os
from .base import BaseProjectGenerator
from .cmake import DefaultArgs, Execute
from ..config import GetProjectFolder


def SetupGmakeProjectGenerator(commands):
    command = BaseProjectGenerator(commands, 'gmake',
        help='Generate the generic Unix makefiles.')
    return command

def GenerateGMakeProject(args):
    if not os.path.isdir(args.project):
        os.mkdir(args.project)

    cmakeArgs = DefaultArgs(['-G', 'Unix Makefiles'], args)
    cmakeArgs.append(args.root)

    return Execute(cmakeArgs, args.project)