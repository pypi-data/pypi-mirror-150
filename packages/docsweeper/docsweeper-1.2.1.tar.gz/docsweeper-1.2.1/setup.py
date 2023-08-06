# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['_docsweeper', 'docsweeper', 'flake8_plugin']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.0,<9.0.0']

entry_points = \
{'console_scripts': ['docsweeper = _docsweeper.command_line:parse_args'],
 'flake8.extension': ['DOC100 = flake8_plugin.Plugin:Plugin']}

setup_kwargs = {
    'name': 'docsweeper',
    'version': '1.2.1',
    'description': 'A linter for your Python code base that finds potentially outdated docstrings using version control.',
    'long_description': '============\n Docsweeper\n============\n\n.. image:: https://img.shields.io/pypi/pyversions/docsweeper?style=flat-square\n   :alt: PyPI - Python Version\n   :target: https://pypi.org/project/docsweeper/\n\n.. image:: https://img.shields.io/pypi/v/docsweeper?style=flat-square\n   :alt: PyPI\n   :target: https://pypi.org/project/docsweeper/\n\n.. image:: https://readthedocs.org/projects/docsweeper/badge/?version=stable\n   :target: https://docsweeper.readthedocs.io/en/stable/?badge=stable\n   :alt: Documentation Status\n\n.. image:: https://img.shields.io/pypi/l/docsweeper?style=flat-square\n   :alt: PyPI - License\n   :target: https://pypi.org/project/docsweeper/\n\n*Docsweeper* is a linter for version controlled *Python* code bases that finds\npotentially outdated docstrings. *Docsweeper* interacts with the version control system\nto retrieve a full revision history of a given *Python* source file. For every code\ntoken in the file that has a docstring (see `PEP 257\n<https://peps.python.org/pep-0257/>`_), *Docsweeper* will analyze the version control\nhistory to determine\n\n#. in which revision the docstring has last been changed, and\n#. how often the source code that is referenced by the docstring has been altered since\n   that revision.\n\nThis can help you quickly find potentially outdated docstrings in your *Python* code\nbase.\n\n*Docsweeper* can be used as a stand-alone application or as a plugin for the `Flake8\n<https://flake8.pycqa.org/en/latest/>`_ linter.\n\n*Docsweeper* supports the following version control systems:\n\n- `Git <https://git-scm.com/>`_ v1.7.0 or newer, and\n- `Mercurial <https://www.mercurial-scm.org/>`_ v5.2 or newer.\n\nRefer to the `documentation <https://docsweeper.readthedocs.io/>`_ for more information.\n',
    'author': 'Andreas Thüring',
    'author_email': 'a.thuering@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://docsweeper.readthedocs.io/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
