# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sugaru',
 'sugaru.file_loader',
 'sugaru.file_loader.simple_json',
 'sugaru.file_loader.simple_yaml',
 'sugaru.file_writer',
 'sugaru.file_writer.simple_json',
 'sugaru.file_writer.simple_yaml',
 'sugaru.object_loader',
 'sugaru.plugin_executor',
 'sugaru.utils']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['typer[all]>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'sugaru',
    'version': '0.0.1',
    'description': 'Create your own syntax stupidly simple!',
    'long_description': '# sugaru\n',
    'author': 'Dmitry Makarov',
    'author_email': 'mit.makaroff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
