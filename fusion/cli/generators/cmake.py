import os
import platform
import subprocess
from ..config import GetBuildFolder, GetInstallFolder


def DefaultArgs(makeArgs, args):
    makeArgs.append(Definition('CMAKE_EXPORT_COMPILE_COMMANDS', 'ON'))
    makeArgs.append(Definition('FUSION_BUILD_ARCH', args.arch))

    if args.variant == 'Release':
        makeArgs.append(Definition('CMAKE_BUILD_TYPE', 'MinSizeRel'))
    else:
        makeArgs.append(Definition('CMAKE_BUILD_TYPE', args.variant))

    if hasattr(args, 'toolchain') and args.toolchain is not None:
        toolchainFolder = os.path.join(os.getcwd(), 'cmake', 'toolchains')
        toolchain = args.toolchain
        if not toolchain.endswith('.cmake'):
            toolchain += '.cmake'
        if os.path.isfile(os.path.join(toolchainFolder, toolchain)):
            makeArgs.append(Definition('CMAKE_TOOLCHAIN_FILE',
                os.path.join(toolchainFolder, toolchain)))

    installFolder = os.path.join(os.getcwd(), GetInstallFolder())
    makeArgs.append(
        Definition('CMAKE_INSTALL_PREFIX',
            getattr(args, 'install', installFolder)))

    buildFolder = os.path.join(os.getcwd(), GetBuildFolder())
    makeArgs.append(
        Definition('FUSION_BUILD_ROOT',
            getattr(args, 'build', buildFolder)))

    if hasattr(args, 'definitions') and args.definitions:
        for define in args.definitions:
            [key, value] = SplitDefintion(define)
            makeArgs.append(Definition(key.upper(), value))

    makeArgs.append(
        Definition('OPENSSL_DISABLE_SSL3', 'OFF', 'BOOL'))
    makeArgs.append(
        Definition('OPENSSL_ENABLE_DEPECATED_FEATURES', 'ON', 'BOOL'))
    return makeArgs


def Definition(variable, value, type=None):
    return '-D%(variable)s:%(type)s=%(value)s' % dict(
        variable=str(variable).upper(),
        type=str(type or 'string').upper(),
        value=str(value))


def CMake(command, projectPath, executor):
    command.insert(0, 'cmake')

    print('Using project folder: %s' % projectPath)
    print('Executing CMake command: %s' % ' '.join(command))

    returncode = executor(command, projectPath)
    if returncode == 0:
        return True

    print('CMake run failed with result code: %s' % returncode)
    return False


def SplitDefintion(key):
    value = 1
    try:
        key, value = key.strip().split('=')
    except ValueError:
        pass
    return [key, value]
