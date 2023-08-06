# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['safebag']

package_data = \
{'': ['*']}

install_requires = \
['pytest-cov>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'safebag',
    'version': '0.1.8',
    'description': 'Little python package implementing optional chaining',
    'long_description': '# safebag\n[![Stable Version](https://img.shields.io/pypi/v/safebag?color=black)](https://pypi.org/project/safebag/)\n[![tests](https://github.com/galeNightIn/safebag/workflows/tests/badge.svg)](https://github.com/galeNightIn/safebag)\n\n_Safebag_ is a little python package implementing optional chaining.\n\n## Installation\n\n```bash\npip install safebag\n```\n\n## Usage\n\n### chain [[source](https://github.com/galeNightIn/safebag/blob/69e241022b85b3f4566556f3e3e956d5a750eb20/safebag/_methods.py#L9)]\n\nOptional chain constructor\n\nOptional chain constructed from any object.\n\nChain is used for building sequence of null-safe attribute calls.\n\n```python\nfrom __future__ import annotations\n\nimport dataclasses as dt\nimport typing\n\n\n@dt.dataclass\nclass Node:\n    data: int\n    node: typing.Optional[Node]\n\n\nnodes = Node(data=1, node=Node(data=2, node=None))\n\nfrom safebag import chain\n\nthird_node_proxy = chain(nodes).node.node.node\nprint(third_node_proxy)  # ChainProxy(data_object=None, bool_hook=False)\n```\n\n### get_value [[source](https://github.com/galeNightIn/safebag/blob/69e241022b85b3f4566556f3e3e956d5a750eb20/safebag/_methods.py#L39)]\n\nFinal value getter for optional chain.\n\nOptional chain constructed from any object. Chain is used for building sequence of null-safe attribute calls.\n\n```python\nfrom __future__ import annotations\n\nimport dataclasses as dt\nimport typing\n\n\n@dt.dataclass\nclass Node:\n    data: int\n    node: typing.Optional[Node]\n\n\nnodes = Node(data=1, node=Node(data=2, node=None))\n\nfrom safebag import chain, get_value\n\nthird_node_proxy = chain(nodes).node.node.node\nvalue = get_value(third_node_proxy)\nassert value is None\n\nnext_node = chain(nodes).node\nvalue = get_value(next_node)  # Node(data=2, node=None)\n```\n\nUseful in combination with walrus operator:\n\n```python\nif next_node := chain(nodes).node.node:\n    print(get_value(next_node))\n\nif next_node := chain(nodes).node:\n    print(get_value(next_node))  # Node(data=2, node=None)\n```\n\n### ChainProxy [[source](https://github.com/galeNightIn/safebag/blob/69e241022b85b3f4566556f3e3e956d5a750eb20/safebag/_chain_proxy.py#L11)]\n\n`ChainProxy` container:\n* stores `data_object`\n* proxying `data_object` attribute value into new `ChainProxy` instance\nwhen attribute is invoked. If attribute does not exist or attribute value is `None`.\n`ChainProxy` instance `data_object` will be `None` and `bool_hook` will be `False`.\n* `ChainProxy` instance always returning when attribute is invoked.',
    'author': 'Alexandr Solovev',
    'author_email': 'nightingale.alex.info@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/galeNightIn/safebag',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
