# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ironik',
 'ironik.cli',
 'ironik.config_file_handler',
 'ironik.openstack_handler',
 'ironik.rancher',
 'ironik.util']

package_data = \
{'': ['*'], 'ironik': ['manifests/*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'click>=8.0.0,<9.0.0',
 'kubernetes>=23.3.0,<24.0.0',
 'openstacksdk>=0.61.0,<0.62.0',
 'rich>=10.1.0,<11.0.0']

entry_points = \
{'console_scripts': ['ironik = ironik.__main__:main']}

setup_kwargs = {
    'name': 'ironik',
    'version': '0.1.5',
    'description': 'In Rancher Openstack; Now Install Kubernetes (Ironik); Python CLI Tool for deploying Kubernetes on OpenStack via Rancher.',
    'long_description': "ironik\n===========================\n\n|PyPI| |Python Version| |Read the Docs| |pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/ironik.svg\n   :target: https://pypi.org/project/ironik/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/ironik\n   :target: https://pypi.org/project/ironik\n   :alt: Python Version\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/ironik/latest.svg?label=Read%20the%20Docs\n   :target: https://ironik.readthedocs.io/\n   :alt: Read the documentation at https://ironik.readthedocs.io/\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n.. Warning:: This tool is still in early development and only the core features are available.\n\nFeatures\n--------\n\n- Utilize OpenStack and Rancher APIs to automatically deploy Kubernetes cluster\n- Customize the configuration using templates\n- Install new Kubernetes versions including deploying the external cloud controller manager for OpenStack\n\nInstallation\n------------\n\nYou can install *ironik* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install ironik\n\nAlternatively, *ironik* can also be used as a container to avoid installing it:\n\n.. code:: console\n\n   $ docker run --rm -ti -v $(pwd):/app docker.gitlab.gwdg.de/jonathan.decker1/ironik/cli:latest ironik --help\n\nThis can be abbreviated using an alias:\n\n.. code:: console\n\n   $ alias dironik='docker run --rm -ti -v $(pwd):/app docker.gitlab.gwdg.de/jonathan.decker1/ironik/cli:latest ironik'\n   $ dironik --help\n\nUsage\n-----\n\nPlease see the `Usage Instructions <https://ironik.readthedocs.io/en/latest/cli_usage.html>`_ for details.\n\nKubernetes can also be deployed manually on OpenStack and Rancher.\nSee the `Manual Deployment Instructions <https://ironik.readthedocs.io/en/latest/manual_kubernetes_deployment.html>`_ for a full guide.\n\nTODOs\n-----\n\n- Update Code documentation to use Google code doc style\n- Improve print messages during execution\n- Implement a template validator\n- Implement cluster validation\n- Set up test suite\n- Implement automatic config fetching\n- Add functionality for undoing deployments and other helpful commands\n\nContributing\n------------\n\nContributions are very welcome. To learn more, see the `Contributor Guide`_.\n\n\nCredits\n-------\n\nThis package was created with cookietemple_ using Cookiecutter_ based on Hypermodern_Python_Cookiecutter_.\n\n.. _cookietemple: https://cookietemple.com\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT: http://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern_Python_Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _pip: https://pip.pypa.io/\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://ironik.readthedocs.io/en/latest/usage.html\n",
    'author': 'Jonathan Decker',
    'author_email': 'jonathan.decker@uni-goettingen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.gwdg.de/jonathan.decker1/ironik',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
