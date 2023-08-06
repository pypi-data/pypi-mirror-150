# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cofactr',
 'cofactr.kb.entity',
 'cofactr.schema',
 'cofactr.schema.flagship',
 'cofactr.schema.logistics']

package_data = \
{'': ['*']}

install_requires = \
['urllib3>=1.26.9,<2.0.0']

setup_kwargs = {
    'name': 'cofactr',
    'version': '3.0.1',
    'description': 'Client library for accessing Cofactr data.',
    'long_description': '# Cofactr\n\nPython client library for accessing Cofactr.\n\n## Example\n\n```python\nfrom typing import List\nfrom cofactr.core import get_part, get_parts, search_parts\n# Flagship is the default schema.\nfrom cofactr.schema.flagship.part import Part\n\npart_res = get_part(id=cpid, external=False)\npart: Part = res["data"]\n\nparts_res = search_parts(query="esp32", external=False)\nparts: List[Part] = res["data"]\n```\n',
    'author': 'Noah Trueblood',
    'author_email': 'noah@cofactr.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cofactr/cofactr-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
