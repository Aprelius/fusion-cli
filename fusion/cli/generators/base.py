import os
import platform
from ..config import DefaultArchitecture, DefaultCompiler, DefaultVariant, \
    GetBuildFolder, GetInstallFolder, GetProjectFolder, \
    GetSupportedArchitectures, GetSupportedVariants


def BaseProjectGenerator(commands, *args, **kwargs):
    command = commands.add_parser(*args, **kwargs)
    command.add_argument('-a', '--arch', dest='arch',
        default=DefaultArchitecture(),
        choices=list(GetSupportedArchitectures().keys()),
        help='Force the architecture type of the build.')

    buildFolder = os.path.join(os.getcwd(), GetBuildFolder())
    command.add_argument('--build-path', '-b',
        dest='build',
        metavar='<BUILD PATH>',
        default=buildFolder,
        help='Specify the build path for compiled artifacts.\n' \
             'The default build path is: %s' % buildFolder)

    command.add_argument('--container', '-C', required=False,
        help='Target docker container to use for build if specified.')

    installFolder = os.path.join(os.getcwd(), GetInstallFolder())
    command.add_argument('--install-path', '-i',
        dest='install',
        metavar='<INSTALL PATH>',
        default=installFolder,
        help='Specify the install path if the project should install ' \
             'results.\n' \
             'The default install path is: %s' % installFolder)

    projectFolder = os.path.join(os.getcwd(), GetProjectFolder())
    command.add_argument('--project-path', '-p',
        dest='project',
        metavar='<PROJECT PATH>',
        default=projectFolder,
        help='Specify the project path if the project should setup into.\n' \
             'The default project path is: %s' % projectFolder)

    command.add_argument('-v', '--variant', dest='variant',
        default=DefaultVariant(),
        choices=GetSupportedVariants(),
        help='Specify the variant type of the build. Default is: debug.')
    command.add_argument('--toolchain', '-t', required=False,
        default=DefaultCompiler(platform.system()),
        help='Toolchain to build the project with.\n' \
             'Default toolchain is: %s' % DefaultCompiler(platform.system()))

    command.add_argument('--defintion', '-D_', dest='definitions', action='append',
        help='Add a definition which will be passed to the CMake generator.')
    return command
