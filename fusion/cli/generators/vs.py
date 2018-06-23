import platform
from .base import BaseProjectGenerator
from .cmake import DefaultArgs, Execute
from ..config import GetSupportedArchitectures


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


def GenerateVSProject(args):
    architectures = {
        'x86_64': 'Win64',
        'i386': 'Win32'
    }

    versions = {
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

    version = 'Visual Studio %s %s %s' % (version, year, arch)
    cmakeArgs = DefaultArgs(['-G', '"%s"' % version], args)
    cmakeArgs.append(args.root)

    return Execute(cmakeArgs, args.project)