from .base import BaseProjectGenerator
from .gmake import GenerateGMakeProject, SetupGmakeProjectGenerator
from .vs import GenerateVSProject, SetupVSProjectGenerator
from .xcode import GenerateXCodeProject, SetupXCodeProjectGenerator

__all__ = [
    'BaseProjectGenerator',
    'GenerateGMakeProject', 'SetupGmakeProjectGenerator',
    'GenerateVSProject', 'SetupVSProjectGenerator',
    'GenerateXCodeProject', 'SetupXCodeProjectGenerator',
    'SetupProjectGenerators',
    'RunGenerator']

from ..config import GetSupportedVisualStudioVersions
from ..utilities import ValidateRootPath


def SetupProjectGenerators(commands, system):
    if system == 'Windows':
        for version in GetSupportedVisualStudioVersions():
            SetupVSProjectGenerator(commands, version,
                help='Generate a Visual Studio %s solution set.' % version)
    elif system == 'Darwin':
        SetupXCodeProjectGenerator(commands)
    if system in ('Linux', 'Darwin'):
        SetupGmakeProjectGenerator(commands)
    return commands


def RunGenerator(command, args, system):
    ValidateRootPath(args.root)
    if command == 'gmake':
        return GenerateGMakeProject(args)
    if command == 'xcode':
        return GenerateXCodeProject(args)
    if command in GetSupportedVisualStudioVersions():
        return GenerateVSProject(args)
    return False;
