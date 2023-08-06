# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['main_entrypoint']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'main-entrypoint',
    'version': '0.1.2',
    'description': '',
    'long_description': '# main-entrypoint\n\nA decorator to avoid `if __name__ == "__main__":`\n\n```python\nfrom main_entrypoint import entrypoint\n\n@entrypoint\ndef main():\n    print("Hello World")\n```\n\n```bash\n$ python my_script.py\nHello World\n\n$ python -c "import my_script"\n# no output\n```\n\n## Installation\n\n```bash\npip install main-entrypoint\n```\n',
    'author': 'Jonathan Striebel',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jstriebel/main-entrypoint',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
