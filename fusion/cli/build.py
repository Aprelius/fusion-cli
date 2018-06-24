import os
import platform
import subprocess
from .config import DefaultArchitecture, DefaultVariant, \
    GetProjectFolder, GetSupportedArchitectures, GetSupportedVariants
from .exceptions import ProjectNotInitialized
from .generators import GenerateGMakeProject
from .utilities import ValidateRootPath


def SetupBuildCommand(commands):
    command = commands.add_parser('build', help='Build the project.')
    command.add_argument('--arch', '-a', required=False,
        choices=list(GetSupportedArchitectures().keys()),
        default=DefaultArchitecture(),
        help='Specify the architecture to build. Default: %s' % \
            DefaultArchitecture())

    command.add_argument('--concurrency', '-c', type=int, default=1,
        required=False,
        help='Specify the concurrency for building. Only used when executing '\
            'make on a POSIX system.')

    projectFolder = os.path.join(os.getcwd(), GetProjectFolder())
    command.add_argument('--project-path', '-p',
        dest='project',
        metavar='<PROJECT PATH>',
        default=projectFolder,
        help='Specify the project path if the project should setup into.\n' \
             'The default project path is: %s' % projectFolder)

    command.add_argument('--variant', '-v', required=False,
        choices=list(GetSupportedVariants()),
        default=DefaultVariant(),
        help='Specify the variant to build. Default: %s' % DefaultVariant())
    command.add_argument('--toolchain', '-t', required=False)
    command.add_argument('--verbose', action='store_true', default=False,
        help='Trigger verbose logging during the build process.')
    return command


def Make(command, projectPath):
    command.insert(0, 'make')

    print('Using project folder: %s' % projectPath)
    print('Executing Make command: %s' % ' '.join(command))

    if platform.system() == 'Windows':
        command = ' '.join(command)
    try:
        process = subprocess.Popen(command,
            cwd=projectPath, stdout=subprocess.PIPE, bufsize=1)
        while True:
            if process.poll() is not None:
                break
            for line in iter(process.stdout.readline, b''):
                print(line.strip())
    except OSError:
        raise

    returncode = process.poll()
    if returncode == 0:
       return True

    print('Make run failed with result code: %s' % returncode)
    return False


def RunBuild(args):
    ValidateRootPath(args.root)

    if not os.path.isdir(args.project):
        success = False
        if platform.system() == 'Linux':
            success = GenerateGMakeProject(args)
        if not success:
            raise ProjectNotInitialized(args.project)

    makeArgs = ['-j%d' % args.concurrency]
    if args.verbose:
        makeArgs.append('VERBOSE=1')
    return Make(makeArgs, args.project)