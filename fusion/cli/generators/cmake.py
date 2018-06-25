import os
import platform
import subprocess
from ..config import GetBuildFolder, GetInstallFolder


def DefaultArgs(makeArgs, args):
    makeArgs.append(Definition('CMAKE_EXPORT_COMPILE_COMMANDS', 'ON'))
    makeArgs.append(Definition('CMAKE_BUILD_TYPE', args.variant))
    makeArgs.append(Definition('FUSION_BUILD_ARCH', args.arch))

    if hasattr(args, 'toolchain') and args.toolchain is not None:
        toolchainFolder = os.path.join(os.getcwd(), 'cmake', 'toolchains')
        toolchain = args.toolchain
        if not toolchain.endswith('.cmake'):
            toolchain += '.cmake'
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
    return makeArgs


def Definition(variable, value, type=None):
    return '-D%(variable)s:%(type)s=%(value)s' % dict(
        variable=str(variable).upper(),
        type=str(type or 'string').upper(),
        value=str(value))


def Execute(command, projectPath):
    command.insert(0, 'cmake')

    print('Using project folder: %s' % projectPath)
    print('Executing CMake command: %s' % ' '.join(command))

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

    print('CMake run failed with result code: %s' % returncode)
    return False