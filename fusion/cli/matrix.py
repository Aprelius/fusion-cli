import configparser as ConfigParser
import os
from os.path import exists, join
import platform
from .docker import RunAsContainer
from .exceptions import MatrixValidationError
from .utilities import Execute

DEFAULT_MATRIX_FILE = 'matrix.ini'


class MatrixEntry(object):
    def __init__(self, target, arch, toolchain, variant):
        self.target = target
        self.arch = arch
        self.toolchain = toolchain
        self.variant = variant
        self.container = None
        self.priority = 1

    def __repr__(self):
        return self.name

    @property
    def name(self):
        return '{}-{}-{}-{}'.format(self.target, self.arch, self.toolchain, self.variant)

def SetupBuildMatrixCommand(commands):
    command = commands.add_parser('build-matrix',
        help='Build the project matrix as psecified by a matrix configuration.')
    command.add_argument('--all', action='store_true', default=False, required=False,
        help='Run all entries in the build matrix for the current platform.')
    command.add_argument('--concurrency', '-c', type=int, default=1,
        required=False,
        help='Specify the concurrency for building. Only used when executing '\
            'make on a POSIX system.')
    command.add_argument('--config', '-C', default=join(os.getcwd(), DEFAULT_MATRIX_FILE),
        required=False,
        help='Path to the matrix configuration. If one is not specified then '
             'the default location is to look in the project root for it.')
    command.add_argument('--fresh', action='store_true', default=False,
        help='Regenerate the CMake project for the build.')
    command.add_argument('--priority', '-p', type=int, default=1, required=False,
        help='Specify a build matrix priority to filter on. By default only priority '
             '1 items will be built.')
    command.add_argument('--verbose', '-v', action='store_true', default=False,
        help='Trigger verbose logging during the build process.')
    return command

def ParseMatrixConfig(configFile):
    config = configparser.ConfigParser()
    with open(configFile, 'rb') as handle:
        config.readfp(handle)

    target = str(platform.system()).lower()
    if not config.has_section(target):
        print('No matrix configuration for platform: {}'.format(target))
        return False

    arch = ValidateTarget(config, target, 'arch')
    toolchain = ValidateTarget(config, target, 'toolchain')
    variant = ValidateTarget(config, target, 'variant')

    matrix = []
    for a in arch:
        for t in toolchain:
            for v in variant:
                entry = MatrixEntry(target, a, t, v)
                matrix.append([entry.name, entry])

    options = [('priority', config.getint), ('container', config.get)]
    for section in config.sections():
        filters = section.split('-')
        if len(filters) != 4:
            continue

        for _, entry in matrix:
            if filters[0] != '*' and entry.target != filters[0]:
                continue
            if filters[1] != '*' and entry.arch != filters[1]:
                continue
            if filters[2] != '*' and entry.toolchain != filters[2]:
                continue
            if filters[3] != '*' and entry.variant != filters[3]:
                continue
            for option, method in options:
                if not config.has_option(section, option):
                    continue
                value = method(section, option)
                setattr(entry, option, value)

    return True, matrix

def RunBuildMatrix(args):
    if not exists(args.config):
        print('Matrix configuration does not exists at: {}'.format(args.config))
        return False

    try:
        success, matrix = ParseMatrixConfig(args.config)
    except MatrixValidationError as e:
        print(e.message)
        return False

    if not success:
        return False

    parameters = dict(concurrency=args.concurrency, fresh=args.fresh,
        verbose=args.verbose)

    for identifier, entry in matrix:
        if not args.all and entry.priority > args.priority:
            continue
        command = [
            'build',
            '--arch={}'.format(entry.arch),
            '--variant={}'.format(entry.variant.title()),
            '--toolchain={}'.format(entry.toolchain),
            '--concurrency={}'.format(args.concurrency)
        ]
        print('Building matrix entry: {}'.format(identifier))
        if args.verbose:
            print('Executing with parameters: {}'.format(' '.join(command)))
            if entry.container:
                print('Using container: {}'.format(entry.container))
        if entry.container:
            if not RunAsContainer(parameters, command, entry.container):
                print('Matrix build failed for target (container={}): {}'.format(
                    entry.container, identifier))
                return False
        else:
            command.insert(0, 'fusion-cli')
            if not Execute(command, os.getcwd()):
                print('Matrix build failed for target: {}'.format(identifier))
                return False

    return True


def ValidateTarget(config, target, option):
    if not config.has_option(target, option):
        message = "Matrix configuration for '{}' does not specify: {}".format(
            target, option)
        raise MatrixValidationError(message)

    values = config.get(target, option, True).strip()
    if not values:
        print("Option list for '{}' on target '{}' is empty".format(option, target))
        return False

    return values.split()
