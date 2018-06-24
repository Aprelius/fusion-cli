import os
import shutil
import tempfile
import traceback
from fusion.cli.utilities import RenderTemplate

__all__ = ['CreateExecutable', 'SetupExecutableCreator']


def SetupExecutableCreator(commands):
    command = commands.add_parser('create-executable',
        help='Generate a CMake executable project and add it to the CMake '
             'build pipeline.')
    command.add_argument('--name', '-n', required=True,
        help='Name of the executable to create.')
    command.add_argument('location',
        help='Location to write the executable project too')
    return command


def CreateExecutableFolder(exePath, name):
    includePath = os.path.join(exePath, 'include')
    os.mkdir(includePath)

    headerPath = os.path.join(includePath, 'fusion', 'example')
    os.makedirs(headerPath)

    # Executable header template
    context = dict(exeName=name)
    content = RenderTemplate('executable/ExecutableHeader.template', **context)
    fileName = os.path.join(headerPath, '%s.h' % name)
    with open(fileName, 'wb') as handle:
        handle.write(content)

    sourcePath = os.path.join(exePath, 'src')
    os.mkdir(sourcePath)

    # Executable main template
    content = RenderTemplate('executable/ExecutableMain.template', **context)
    fileName = os.path.join(sourcePath, 'main.cpp')
    with open(fileName, 'wb') as handle:
        handle.write(content)

    # CMakeLists.txt template file
    content = RenderTemplate('executable/CMakeLists.template', **context)
    cmakeFile = os.path.join(exePath, 'CMakeLists.txt')
    with open(cmakeFile, 'wb') as handle:
        handle.write(content)


def CreateExecutable(args):
    print('Creating executable: %s' % args.name)

    fullPath = args.location
    if not os.path.isabs(args.location):
        fullPath = os.path.join(args.root, args.location)
    exePath = os.path.join(fullPath, args.name)
    if not os.path.exists(fullPath):
        os.makedirs(fullPath)
    elif os.path.exists(exePath):
        print("Executable path '%s' already exists" % args.name)
        return False

    # We write all of the output to a temporary directory. If for some
    # reason there are any failures, we will just nuke the temporary
    # directory on exit.
    tempdir = tempfile.mkdtemp()

    try:
        try:
            CreateExecutableFolder(tempdir, args.name)
        except Exception:
            traceback.print_exc()
            return False

        # Rename the temporary directory to the new location so that the
        # generated artifacts are added to the build pipeline.
        shutil.move(tempdir, exePath)
    finally:
        try:
            if os.path.exists(tempdir):
                shutil.rmtree(tempdir)
        except (IOError, OSError):
            pass

    # At this point we can start adding the new executable to the main
    # project pipeline.
    cmakeParent = os.path.join(fullPath, 'CMakeLists.txt')
    if not os.path.isfile(cmakeParent):
        print('Parent path is not a CMake directory. Skipping adding the new ' \
              'executable to the project.')
    else:
        with open(cmakeParent, 'rb') as handle:
            content = handle.read()
        with open(cmakeParent, 'wb') as handle:
            handle.write(content.strip())
            handle.write('\nadd_subdirectory(%s)\n' % args.name)
        print("Successfully added '%s' to parent CMakeLists.txt" % args.name)

    print('Successfully wrote project files.')
    return True