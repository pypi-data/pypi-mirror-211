# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spei', 'spei.resources']

package_data = \
{'': ['*']}

install_requires = \
['cryptography==3.4.7',
 'lxml>=4.9.1,<5.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'spei-python',
    'version': '0.7.1',
    'description': '',
    'long_description': '[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nspei-python\n===========\n\nA library for accessing the SPEI API for python.\n\n\n## Installation\nUse the package manager [poetry](https://pypi.org/project/poetry/) to install.\n\n    poetry install spei-python\n\n## Test\nTested with [mamba](https://mamba-framework.readthedocs.io/en/latest/), install poetry dev packages and then run tests.\n\n    poetry run make test\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n\n## Checksum Generator\nThis repo includes a utility to generate [firma digital aplicada](https://www.notion.so/fondeadoraroot/Algoritmo-de-Firma-e-Karpay-SPEI-02e6c25b7c5943bea054ae37c9605bdc)\n\n```sh\npython bin/generate_checksum.py bin/message.json\n```\n',
    'author': 'gonz',
    'author_email': 'gonzasestopal@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
