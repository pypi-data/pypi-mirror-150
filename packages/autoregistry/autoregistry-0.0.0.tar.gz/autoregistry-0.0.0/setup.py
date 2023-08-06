# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autoregistry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'autoregistry',
    'version': '0.0.0',
    'description': '',
    'long_description': '.. image:: assets/logo_200w.png\n\n|GHA tests| |Codecov report| |readthedocs|\n\n.. inclusion-marker-do-not-remove\n\nautoregistry\n==============\n\nautoregistry is a\n\n\nFeatures\n========\n\nInstallation\n============\n\n.. code-block:: bash\n\n   python -m pip install git+https://github.com/BrianPugh/autoregistry.git\n\n\nUsage\n=====\n\n.. code-block:: python\n\n   import autoregistry\n\n\n\n\n.. |GHA tests| image:: https://github.com/BrianPugh/autoregistry/workflows/tests/badge.svg\n   :target: https://github.com/BrianPugh/autoregistry/actions?query=workflow%3Atests\n   :alt: GHA Status\n.. |Codecov report| image:: https://codecov.io/github/BrianPugh/autoregistry/coverage.svg?branch=main\n   :target: https://codecov.io/github/BrianPugh/autoregistry?branch=main\n   :alt: Coverage\n.. |readthedocs| image:: https://readthedocs.org/projects/autoregistry/badge/?version=latest\n        :target: https://autoregistry.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n',
    'author': 'Brian Pugh',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
