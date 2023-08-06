# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['poetry_artifactregistry_plugin']

package_data = \
{'': ['*']}

install_requires = \
['keyrings.google-artifactregistry-auth>=1.0.0,<2.0.0',
 'poetry>=1.2.0b1dev0,<2.0.0']

entry_points = \
{'poetry.plugin': ['demo = '
                   'poetry_artifactregistry_plugin.plugins:ArtifactRegistryPlugin']}

setup_kwargs = {
    'name': 'poetry-artifactregistry-plugin',
    'version': '0.1.0',
    'description': 'This repository is a plugin to configure poetry and Google Artifact Registry authentication',
    'long_description': '',
    'author': 'Julien Klaer',
    'author_email': 'klaer.julien@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
