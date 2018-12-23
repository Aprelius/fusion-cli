import os
import platform
from .base import BaseProjectGenerator
from .cmake import DefaultArgs, CMake
from ..config import GetProjectFolder
from ..docker import RunAsContainer
from ..utilities import Execute


def SetupGmakeProjectGenerator(commands):
    command = BaseProjectGenerator(commands, 'gmake',
        help='Generate the generic Unix makefiles.')
    return command


def ProjectPath(args, basePath=None):
    projectPath = '%(platform)s-%(arch)s-%(toolchain)s-%(variant)s' % dict(
        platform=str(platform.system()).lower(),
        arch=args.arch,
        toolchain=getattr(args, 'toolchain', 'unknown').lower(),
        variant=str(args.variant).lower())

    if basePath is None:
        return projectPath
    return os.path.join(basePath, projectPath)


def GenerateGMakeProject(args):
    if not os.path.isdir(args.project):
        os.mkdir(args.project)

    projectPath = ProjectPath(args, args.project)

    if not os.path.isdir(projectPath):
        os.mkdir(projectPath)

    if args.container:
        return RunAsContainer(args, args.command)

    cmakeArgs = DefaultArgs([], args)
    cmakeArgs.extend(['-G', 'Unix Makefiles'])
    cmakeArgs.append(args.root)

    return CMake(cmakeArgs, projectPath, Execute)
