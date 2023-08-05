# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['otf', 'otf.pack']

package_data = \
{'': ['*']}

extras_require = \
{'msgpack': ['msgpack>=1.0.2,<2.0.0']}

setup_kwargs = {
    'name': 'otf',
    'version': '0.1.0a5',
    'description': 'A python framework for on-the-fly distributed workflows',
    'long_description': 'On-the-fly distributed python workflows\n=======================================\n\n|PyPI| |PyPI - Python Version| |License: CC0-1.0| |Tests| |codecov|\n|Documentation Status| |binder|\n\nOTF is a framework to programmatically write, run and debug workflows.\n\nNotebooks:\n----------\n\nOTF is still in its infancy. We currently mostly rely on notebook to demonstrate\nhow it works:\n\n+ `Introduction <https://nbviewer.org/github/till-varoquaux/otf/blob/HEAD/docs/examples/introduction.ipynb>`_\n+ `Serialisation <https://nbviewer.org/github/till-varoquaux/otf/blob/HEAD/docs/examples/serialisation.ipynb>`_\n\n\nInstalling\n----------\n\nOTF is currently in pre-alpha. If you really want to play with it you\ncan check install the latest build via:\n\n.. code:: bash\n\n   $ pip install -i https://test.pypi.org/simple/ otf\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/otf.svg\n   :target: https://pypi.org/project/otf/\n.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/otf\n.. |License: CC0-1.0| image:: https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg\n   :target: http://creativecommons.org/publicdomain/zero/1.0/\n.. |Tests| image:: https://github.com/till-varoquaux/otf/actions/workflows/ci.yml/badge.svg?branch=main\n   :target: https://github.com/till-varoquaux/otf/actions/workflows/ci.yml\n.. |codecov| image:: https://codecov.io/gh/till-varoquaux/otf/branch/main/graph/badge.svg?token=ahhI117oFg\n   :target: https://codecov.io/gh/till-varoquaux/otf\n.. |Documentation Status| image:: https://readthedocs.org/projects/otf/badge/?version=latest\n   :target: https://otf.readthedocs.io/en/latest/?badge=latest\n.. |binder| image:: https://mybinder.org/badge_logo.svg\n   :target: https://mybinder.org/v2/gh/till-varoquaux/otf/HEAD?labpath=docs%2Fexamples%2Fintroduction.ipynb\n',
    'author': 'Till Varoquaux',
    'author_email': 'till.varoquaux@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/till-varoquaux/otf',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
