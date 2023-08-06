# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['object_colors']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'object-colors',
    'version': '2.1.0',
    'description': 'Object-oriented library for stylizing terminal output',
    'long_description': 'object-colors\n=============\n.. image:: https://img.shields.io/badge/License-MIT-yellow.svg\n    :target: https://opensource.org/licenses/MIT\n    :alt: License\n.. image:: https://img.shields.io/pypi/v/object-colors\n    :target: https://img.shields.io/pypi/v/object-colors\n    :alt: pypi\n.. image:: https://github.com/jshwi/object-colors/actions/workflows/ci.yml/badge.svg\n    :target: https://github.com/jshwi/object-colors/actions/workflows/ci.yml\n    :alt: CI\n.. image:: https://github.com/jshwi/object-colors/actions/workflows/codeql-analysis.yml/badge.svg\n    :target: https://github.com/jshwi/object-colors/actions/workflows/codeql-analysis.yml\n    :alt: CodeQL\n.. image:: https://codecov.io/gh/jshwi/object-colors/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jshwi/object-colors\n    :alt: codecov.io\n.. image:: https://readthedocs.org/projects/object-colors/badge/?version=latest\n    :target: https://object-colors.readthedocs.io/en/latest/?badge=latest\n    :alt: readthedocs.org\n.. image:: https://img.shields.io/badge/python-3.8-blue.svg\n    :target: https://www.python.org/downloads/release/python-380\n    :alt: python3.8\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: black\n\nObject-oriented library for stylizing terminal output\n-----------------------------------------------------\n\nInstallation\n------------\n\n.. code-block:: console\n\n    $ pip install object-colors\n..\n\nUsage\n-----\n\nImport the ``Color`` object from ``object_colors``\n\n.. code-block:: python\n\n    >>> from object_colors import Color\n\nArgs can be provided as strings or as indices corresponding to their index in an ANSI escape sequence\n\n.. code-block:: python\n\n    >>> Color(effect="bold", fore="red", back="green")\n    Color(effect=1, fore=1, back=2, objects())\n\nThe following would yield the same result\n\n.. code-block:: python\n\n    >>> Color(effect=1, fore=1, back=2)\n    Color(effect=1, fore=1, back=2, objects())\n\nThe above options are part of the below mapping\n\n.. code-block:: python\n\n    >>> for i, c in enumerate(Color.colors):\n    ...     print(i, c)\n    0 black\n    1 red\n    2 green\n    3 yellow\n    4 blue\n    5 magenta\n    6 cyan\n    7 white\n\n.. code-block:: python\n\n    >>> for i, e in enumerate(Color.effects):\n    ...     print(i, e)\n    0 none\n    1 bold\n    2 dim\n    3 italic\n    4 underline\n    5 blink\n    6 blinking\n    7 negative\n    8 empty\n    9 strikethrough\n\n\nTo configure the current object either ``effect``, ``fore``, or ``back`` can be provided\n\nThey must be an ``int``, ``str``, or ``None`` type\n\n.. code-block:: python\n\n    >>> c = Color()\n    >>> c.set(effect="bold", fore="red", back="red")\n    >>> c\n    Color(effect=1, fore=1, back=1, objects())\n\nCreate new objects with by providing a ``dict`` object with any keyword argument\n\nUse ``set`` to set multiple parameters\n\n.. code-block:: python\n\n    >>> c = Color()\n    >>> c.set(bold_green=dict(effect="bold", fore="green"))\n    >>> c\n    Color(effect=None, fore=None, back=None, objects(bold_green))\n\nReturn ``str`` or ``tuple`` using ``get``\n\n.. code-block:: python\n\n    >>> c = Color()\n    >>> c.set(red=dict(fore="red"))\n    >>> c.set(yellow=dict(fore="yellow"))\n    >>> f"{c.red.get(\'*\')} {c.yellow.get(\'Warning\')}"\n    \'\\x1b[31m*\\x1b[0;0m \\x1b[33mWarning\\x1b[0;0m\'\n\n.. code-block:: python\n\n    >>> c = Color()\n    >>> c.set(red=dict(fore="red"))\n    >>> xyz = c.red.get("x", "y", "z")\n    >>> xyz\n    (\'\\x1b[31mx\\x1b[0;0m\', \'\\x1b[31my\\x1b[0;0m\', \'\\x1b[31mz\\x1b[0;0m\')\n    >>> x, y, z = xyz\n    >>> f"{x} {y} {z}"\n    \'\\x1b[31mx\\x1b[0;0m \\x1b[31my\\x1b[0;0m \\x1b[31mz\\x1b[0;0m\'\n\nPrint the result using ``print``\n\n.. code-block:: python\n\n    >>> c = Color(effect="bold", fore="cyan")\n    >>> # doctest strips ansi codes from print\n    >>> c.print("bold cyan")  # \'\\x1b[1;36mbold cyan\\x1b[0;0m\'\n    bold cyan\n\nLoad all ``effect``, ``fore``, or ``back`` elements using ``populate()``\n\n.. code-block:: python\n\n    >>> c = Color()\n    >>> c.populate("fore")\n    >>> c\n    Color(effect=None, fore=None, back=None, objects(black, red, green, yellow, blue, magenta, cyan, white))\n\n.. code-block:: python\n\n    >>> c = Color()\n    >>> c.set(red=dict(fore="red"))\n    >>> c.red.populate("effect")\n    >>> c.red\n    Color(effect=None, fore=1, back=None, objects(none, bold, dim, italic, underline, blink, blinking, negative, empty, strikethrough))\n    >>> # doctest strips ansi codes from print\n    >>> c.red.strikethrough.print("strikethrough red")  # \'\\x1b[9;31mstrikethrough red\\x1b[0;0m\'\n    strikethrough red\n',
    'author': 'jshwi',
    'author_email': 'stephen@jshwisolutions.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
