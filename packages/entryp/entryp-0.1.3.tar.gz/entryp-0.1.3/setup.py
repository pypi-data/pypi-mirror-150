# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['entryp']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'entryp',
    'version': '0.1.3',
    'description': '',
    'long_description': '# main-entrypoint\n\n[![PyPI version](https://img.shields.io/pypi/v/main-entrypoint)](https://pypi.python.org/pypi/main-entrypoint)\n[![Supported Python Versions](https://img.shields.io/pypi/pyversions/main-entrypoint.svg)](https://pypi.python.org/pypi/main-entrypoint)\n[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nA decorator to avoid `if __name__ == "__main__":`, instead use\n\n```python\nfrom main_entrypoint import entrypoint\n\n@entrypoint\ndef main():\n    print("Hello World")\n```\n\n```bash\n$ python my_script.py\nHello World\n\n$ python -c "import my_script"\n# no output\n```\n\n\n## Installation\n\n```bash\npip install main-entrypoint\n```\n\n\n## Details\n\nSpecifying the `@entrypoint` decorator on a function `my_func` can be considered equivalent to running\n```python\nif __name__ == "__main__":\n    my_func()\n```\nat the end of the same module.\n\nIf the decorator is used multiple times in the same file, the functions are executed in the order they are defined.\n\nThe default `entrypoint` decorator uses the [`atexit` module](https://docs.python.org/library/atexit.html). Simple usage of registered atexit functions still works as expected, but involved workflows (e.g. specific exception-flows) relying on atexit behaviour might:tm: break. In those cases, please consider to use one of the two other available modes, `first_rerun_remaining` and `immediate`, e.g.\n\n```python\nfrom main_entrypoint import entrypoint\n\n@entrypoint(mode="immediate")\ndef main():\n    print("Hello World")\n```\n\n`immediate` calls the decorated function immediately, entities defined later in the module will not be available, so moving the function to the end of the module is encouraged. `first_rerun_remaining` will effectively run everything after the decorated function twice, so the code should be free of side-effects and preferably only consist of definitions in this case. The default mode is `at_exit` and should be considered as a first choice.\n\n## Future Work\n\n- [ ] tests\n- [ ] automating formatting, checking and releases\n- [ ] allow to pass arguments to the entrypoint function\n\n\n## License\n\n[MIT](LICENSE)\n',
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
