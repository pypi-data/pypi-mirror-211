import os
from pathlib import Path
from jinja2 import Environment, Template, FileSystemLoader, PackageLoader


def find_template(tmp):

    current_dir = os.path.dirname(os.path.realpath(__file__))

    env = Environment(loader=PackageLoader('edaplore.html_templates', 'templates'))

    template = env.get_template(tmp)

    return template

