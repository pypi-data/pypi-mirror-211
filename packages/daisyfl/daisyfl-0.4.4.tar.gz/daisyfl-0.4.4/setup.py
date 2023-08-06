# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src/py'}

packages = \
['daisyfl',
 'daisyfl.client',
 'daisyfl.client.grpc_client',
 'daisyfl.common',
 'daisyfl.operator',
 'daisyfl.operator.base',
 'daisyfl.operator.base_async',
 'daisyfl.operator.msg_demo',
 'daisyfl.operator.sec_agg',
 'daisyfl.operator.strategy',
 'daisyfl.operator.utils',
 'daisyfl.proto',
 'daisyfl.server',
 'daisyfl.server.grpc_server',
 'daisyfl.simulation',
 'daisyfl.simulation.ray_transport',
 'daisyfl.utils']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.2.2,<3.0.0',
 'cryptography>=38.0.4,<39.0.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'grpcio>=1.43.0,<2.0.0',
 'iterators>=0.0.2,<0.0.3',
 'numpy>=1.21.0,<2.0.0',
 'protobuf>=3.19.0,<4.0.0',
 'pycryptodome>=3.16.0,<4.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=4.0.0,<5.0.0'],
 'simulation': ['ray[default]>=2.0.0,<2.1.0']}

setup_kwargs = {
    'name': 'daisyfl',
    'version': '0.4.4',
    'description': 'Daisy - A Hierarchical Friendly Federated Learning Framework For Edge Computing',
    'long_description': "# Daisy - A Hierarchical Friendly Federated Learning Framework For Edge Computing\n\n## dev mode\n1. clone the source code\n```\ngit clone https://github.com/Intelligent-Systems-Lab/daisy\n```\n2. build up environment\n```\ndocker run -it -v <daisy_source_code>:/root/daisy tcfwbper/daisyfl-dev:<version_tag> /bin/bash\n```\n3. develop<br>\n4. setup examples<br>\ndon't overwrite daisyfl dependency in this step.<br>\n```\ndocker attach <container_id>\n```\n```\ncd <example_path> && conda activate daisy\npip install <pkgs_for_your_example>\n```\n5. run examples\n\n## user mode\n1. install daisyfl\n```\npip install <daisyfl_version>\n```\n2. setup examples\n```\npip install <pkgs_for_your_example>\n```\n3. run examples",
    'author': 'tcfwbper',
    'author_email': 'b05208031@ntu.edu.tw',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Intelligent-Systems-Lab/daisy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
