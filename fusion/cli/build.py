import os
import platform
import shutil
import subprocess
from .config import DefaultArchitecture, DefaultCompiler, DefaultVariant, \
    GetProjectFolder, GetSupportedArchitectures, GetSupportedVariants
from .docker import RunAsContainer
from .exceptions import InvalidRootPath, ProjectNotInitialized
from .generators import GenerateGMakeProject
from .generators.gmake import ProjectPath
from .utilities import Execute, ValidateRootPath


def SetupBuildCommand(commands):
    command = commands.add_parser('build', help='Build the project.')
    command.add_argument('--arch', '-a', required=False,
        choices=list(GetSupportedArchitectures().keys()),
        default=DefaultArchitecture(),
        help='Specify the architecture to build. Default: {}'.format(DefaultArchitecture()))

    command.add_argument('--concurrency', '-c', type=int, default=1,
        required=False,
        help='Specify the concurrency for building. Only used when executing '\
            'make on a POSIX system.')

    command.add_argument('--container', '-C', required=False,
        help='Target docker container to use for build if specified.')

    command.add_argument('--fresh', action='store_true', default=False,
        help='Regenerate the CMake project for the build.')

    projectFolder = os.path.join(os.getcwd(), GetProjectFolder())
    command.add_argument('--project-path', '-p',
        dest='project',
        metavar='<PROJECT PATH>',
        default=projectFolder,
        help='Specify the project path if the project should setup into.\n' \
             'The default project path is: {}'.format(projectFolder))

    command.add_argument('--variant', '-v', required=False,
        choices=list(GetSupportedVariants()),
        default=DefaultVariant(),
        help='Specify the variant to build. Default: {}'.format(DefaultVariant()))
    command.add_argument('--toolchain', '-t', required=False,
        default=DefaultCompiler(platform.system()),
        help='Toolchain to build the project with.\n' \
             'Default toolchain is: {}'.format(DefaultCompiler(platform.system())))
    command.add_argument('--verbose', action='store_true', default=False,
        help='Trigger verbose logging during the build process.')

    command.add_argument('--defintion', '-D', dest='definitions', action='append',
        help='Add a definition which will be passed to the CMake generator.')
    return command


def Make(command, projectPath, executor):
    command.insert(0, 'make')

    print('Using project folder: {}'.format(projectPath))
    print('Executing Make command: {}'.format(' '.join(command)))

    returncode = executor(command, projectPath)
    if returncode == 0:
        return True

    print('Make run failed with result code: {}'.format(returncode))
    return False


def RunBuild(args):
    ValidateRootPath(args.root)

    if args.container:
        return RunAsContainer(args, args.command)

    projectPath = ProjectPath(args, args.project)
    isRefresh = (args.fresh or os.path.isdir(projectPath))

    if args.fresh:
        print('Fusion-CLI: Cleaning out project for fresh CMake run.')
        try:
            if os.path.isdir(projectPath):
                shutil.rmtree(projectPath)
        except (IOError, OSError):
            print('Failed to clean project path')
            return False
        if os.path.isdir(projectPath):
            raise InvalidRootPath()

    success = False
    if platform.system() in ('Darwin', 'Linux'):
        success = GenerateGMakeProject(args)
    if not success:
        if isRefresh:
            print('Failed to re-initialize CMake pipeline.')
            return False
        raise ProjectNotInitialized(projectPath)

    makeArgs = [ '-j{}'.format(args.concurrency) ]
    if args.verbose:
        makeArgs.append('VERBOSE=1')

    return Make(makeArgs, projectPath, Execute)
