# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['print_color_text']
setup_kwargs = {
    'name': 'print-color-text',
    'version': '1.0',
    'description': "one function 'color_print(text, color)'",
    'long_description': None,
    'author': 'MrBedrockpy',
    'author_email': 'aleksejorazbaev28@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
