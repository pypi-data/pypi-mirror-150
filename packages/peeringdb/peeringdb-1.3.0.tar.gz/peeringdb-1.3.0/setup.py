# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['peeringdb', 'peeringdb._debug', 'peeringdb.output']

package_data = \
{'': ['*']}

install_requires = \
['confu>=1,<2', 'munge[yaml,tomlkit]>=1.2.0,<2.0.0', 'twentyc.rpc>=1,<2']

entry_points = \
{'console_scripts': ['peeringdb = peeringdb.cli:main'],
 'markdown.extensions': ['pymdgen = pymdgen.md:Extension']}

setup_kwargs = {
    'name': 'peeringdb',
    'version': '1.3.0',
    'description': 'PeeringDB Django models',
    'long_description': '# peeringdb-py\n\n[![PyPI](https://img.shields.io/pypi/v/peeringdb.svg?maxAge=3600)](https://pypi.python.org/pypi/peeringdb)\n[![Tests](https://github.com/peeringdb/peeringdb-py/workflows/tests/badge.svg)](https://github.com/peeringdb/peeringdb-py)\n[![Codecov](https://img.shields.io/codecov/c/github/peeringdb/peeringdb-py/master.svg?maxAge=3600)](https://codecov.io/github/peeringdb/peeringdb-py)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/peeringdb/peeringdb-py.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/peeringdb/peeringdb-py/context:python)\n\n\nPeeringDB python client\n\nSee http://peeringdb.github.io/peeringdb-py/ for docs\n',
    'author': 'PeeringDB',
    'author_email': 'support@peeringdb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/peeringdb/peeringdb-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
