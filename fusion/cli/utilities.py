TEMPLATE_RENDER_DISABLED = False
try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    TEMPLATE_RENDER_DISABLED = True

import os
from os.path import dirname, join, realpath
import platform
import subprocess
from .exceptions import InvalidRootPath


def Call(command):
    try:
        output = subprocess.check_output(command)
    except subprocess.CalledProcessError:
        return False, ''
    except OSError:
        raise
    return True, output.strip().decode('utf-8')


def Execute(command, workingDirectory):
    if platform.system() == 'Windows':
        command = ' '.join(command)
    try:
        with subprocess.Popen(command,
            cwd=workingDirectory,
            stdout=subprocess.PIPE,
            bufsize=0) as process:
            for line in iter(process.stdout.readline, b''):
                data = str(line.strip(), encoding='utf-8')
                if len(data) > 0:
                    print(data)
    except KeyboardInterrupt:
        pass
    except OSError:
        raise

    return process.poll()


def RenderTemplate(template, **context):
    if TEMPLATE_RENDER_DISABLED:
        raise RuntimeError('Template rendering is disabled without jinja2 installed')
    searchPath = realpath(join(dirname(__file__), 'templates'))
    loader = FileSystemLoader(searchpath=searchPath)
    env = Environment(loader=loader)
    template = env.get_template(template)
    return template.render(**context)


def ValidateRootPath(path):
    if not os.path.exists(path):
        raise InvalidRootPath("Root path '{}' does not exist".format(path))
    cmakeListsFile = os.path.join(path, 'CMakeLists.txt')
    if not os.path.isfile(cmakeListsFile):
        raise InvalidRootPath("Root path '{}' does not conatin a " \
            "CMakeLists.txt file".format(path))
