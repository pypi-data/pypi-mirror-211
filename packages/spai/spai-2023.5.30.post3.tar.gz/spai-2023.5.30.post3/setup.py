# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spai',
 'spai.cli',
 'spai.cli.commands',
 'spai.cli.project-template.apis.analytics',
 'spai.cli.project-template.apis.xyz',
 'spai.cli.project-template.scripts.downloader',
 'spai.cli.project-template.scripts.ndvi',
 'spai.cli.project-template.uis.map',
 'spai.data',
 'spai.data.satellite',
 'spai.data.satellite.sentinelhub',
 'spai.image',
 'spai.image.xyz',
 'spai.storage']

package_data = \
{'': ['*'],
 'spai.cli': ['project-template/*', 'project-template/notebooks/analytics/*']}

install_requires = \
['minio>=7.1.15,<8.0.0', 'pandas>=2.0.2,<3.0.0']

entry_points = \
{'console_scripts': ['spai = spai.main:app']}

setup_kwargs = {
    'name': 'spai',
    'version': '2023.5.30.post3',
    'description': '',
    'long_description': '',
    'author': 'Juan Sensio',
    'author_email': 'it@earthpulse.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
