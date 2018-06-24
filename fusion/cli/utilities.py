TEMPLATE_RENDER_DISABLED = False
try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    TEMPLATE_RENDER_DISABLED = True

import os
from os.path import dirname, join, realpath
from .exceptions import InvalidRootPath


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
        raise InvalidRootPath("Root path '%s' does not exist" % path)
    cmakeListsFile = os.path.join(path, 'CMakeLists.txt')
    if not os.path.isfile(cmakeListsFile):
        raise InvalidRootPath("Root path '%s' does not conatin a " \
            "CMakeLists.txt file")