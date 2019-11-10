import os
import platform
from .base import BaseProjectGenerator
from .cmake import DefaultArgs, CMake
from ..config import GetSupportedArchitectures
from ..docker import RunAsContainer
from ..utilities import Execute

def SetupVSProjectGenerator(commands, *args, **kwargs):
    command = BaseProjectGenerator(commands, *args, **kwargs)
    command.add_argument('--arm', action='store_false', default=False)
    return command


def DetermineMachineType(machine=None):
    architectures = GetSupportedArchitectures()
    machine = machine or platform.machine()

    for arch, supported in architectures.items():
        if machine in supported:
            return arch
    raise RuntimeError('Unsupported architecture: %s' % platform.machine())

def ProjectPath(args, basePath=None):
    projectPath = '%(platform)s-%(arch)s-%(toolchain)s-%(variant)s' % dict(
        platform=str(platform.system()).lower(),
        arch=args.arch,
        toolchain=getattr(args, 'toolchain', 'unknown').lower(),
        variant=str(args.variant).lower())

    if basePath is None:
        return projectPath
    return os.path.join(basePath, projectPath)

def GenerateVSProject(args):
    if not os.path.isdir(args.project):
        os.mkdir(args.project)

    projectPath = ProjectPath(args, args.project)

    if not os.path.isdir(projectPath):
        os.mkdir(projectPath)
    if args.container:
        return RunAsContainer(args, args.command)

    architectures = {
        'x86_64': 'x64',
        'i386': 'Win32'
    }

    versions = {
        'vs2019': ['vc160', 16, 2019],
        'vs2017': ['vc150', 15, 2017],
        'vs2015': ['vc140', 14, 2015],
        'vs2013': ['vc120', 12, 2013]
    }

    try:
        [_, version, year] = versions.get(args.command)
    except ValueError:
        print("Unknown Visual Studio version: %s" % args.command)
        return False

    if args.arm:
        arch = 'ARM'
    else:
        arch = architectures[DetermineMachineType(args.arch)]

    if version >= 16:
        cmakeArgs = DefaultArgs([
            '-G',
            '"Visual Studio %s %s"' % (version, year),
            '-A', arch],
            args)
    else:
        cmakeArgs = DefaultArgs([
            '-G',
            '"Visual Studio %s %s %s"' % (version, year, arch)],
            args)
    cmakeArgs.append(args.root)

    return CMake(cmakeArgs, args.project, Execute)
