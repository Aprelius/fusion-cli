import os
from os.path import join
import platform
from .utilities import Call, Execute


def DockerExecute(container, command, workingDirectory):
    dockerCmd = ['docker', 'run', '-e', 'PYTHONUNBUFFERED=1', '--rm', '-v',
        '%s:/src/build' % workingDirectory, '-w', '/src/build']
    if platform.system() != 'Windows':
        success, uid = Call(['id', '-u'])
        if not success:
            print('WARNING: Failed to retrieve active UID from system.')
        success, gid = Call(['id', '-g'])
        if not success:
            print('WARNING: Failed to retrieve active GID from system.')
        if gid and uid:
            dockerCmd.extend(['-u', '%s:%s' % (uid, gid)])
    dockerCmd.append(container)
    dockerCmd.extend(command)

    print('Executing docker command: %s' % ' '.join(dockerCmd))
    return Execute(dockerCmd, workingDirectory)

def RunAsContainer(args, command):
    commandArgs = ['/src/build/fusion-cli', command]

    allowed = ['toolchain', 'concurrency', 'arch', 'variant']
    flags = ['fresh', 'verbose']

    for key, value in vars(args).items():
        if key in allowed:
            commandArgs.append('--%s=%s' % (key, str(value)))
        elif key in flags and value:
            commandArgs.append('--%s' % key)

    if args.definitions:
        for definition in args.definitions:
            commandArgs.append('-D_%s' % definition)

    return DockerExecute(args.container, commandArgs, os.getcwd())
