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
    return Execute(dockerCmd, workingDirectory) == 0

def RunAsContainer(args, command, container=None):
    commandArgs = ['/src/build/fusion-cli']

    # The 'command' can be passed in either as a single string which
    # will be appended or as a list of arguments which get added to
    # the new command.
    if isinstance(command, list):
        commandArgs.extend(command)
    else:
        commandArgs.append(command)

    allowed = ['toolchain', 'concurrency', 'arch', 'variant']
    flags = ['fresh', 'verbose']

    items = args if isinstance(args, dict) else vars(args)
    for key, value in items.items():
        if key in allowed:
            if key == 'variant':
                value = value.title()
            commandArgs.append('--%s=%s' % (key, str(value)))
        elif key in flags and value:
            commandArgs.append('--%s' % key)

    if hasattr(args, 'definitions'):
        definitions = getattr(args, 'definitions', [])
        for definition in definitions or []:
            commandArgs.append('-D_%s' % definition)

    if not container:
        container = getattr(args, 'container', None)
    if not container:
        print('No container specified')
        return False

    return DockerExecute(container, commandArgs, os.getcwd())
