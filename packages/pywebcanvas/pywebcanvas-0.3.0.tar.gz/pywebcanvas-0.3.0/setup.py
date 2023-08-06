# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywebcanvas']

package_data = \
{'': ['*']}

install_requires = \
['colour>=0.1.5,<0.2.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['pywebcanvas = pywebcanvas.cli:main']}

setup_kwargs = {
    'name': 'pywebcanvas',
    'version': '0.3.0',
    'description': 'A library that allows users to interact with the HTML Canvas with 100% Python + HTML.',
    'long_description': '# pywebcanvas\npywebcanvas is a library that allows users to interact with the HTML Canvas with 100% Python + HTML.\n\n## Getting Started\nJust add the following to an html file and you are ready to go!\n\nBetween the head tags, add pyscript and pywebcanvas:\n```html\n<link rel="stylesheet" href="https://pyscript.net/alpha/pyscript.css" />                                                         \n<script defer src="https://pyscript.net/alpha/pyscript.js"></script>\n<py-env>\n  - pywebcanvas\n</py-env>\n```\n\nIn the body, you can customize the following:\n```python\n<py-script>\nimport pywebcanvas as pwc                                                                                                            \n\ncanvas = pwc.Canvas(800, 600)                                                                                                        \ncanvas.background.fill("blue")                                                                                                       \ntext = pwc.Text(text="Hello World from pywebcanvas!", x=100, y=100, size=25, color="yellow")                                         \ncanvas.render(text)\n</py-script>\n```\n\n## Documentation\nCheckout the following to learn how to use this project:\n- [pywebcanvas](https://gitlab.com/imbev/pywebcanvas)\n- [pyscript](https://github.com/pyscript/pyscript)\n- [pyodide](https://readthedocs.org/projects/pyodide/downloads/pdf/latest/)\n- [python](https://docs.python.org/3/)\n- [html](https://developer.mozilla.org/en-US/docs/Web/HTML)\n\n## Credits\nThis project is made possible by the developers of pyscript, pyodide, and many others.\nLicensed under [LGPL-3.0-or-later](https://gitlab.com/imbev/pywebcanvas/-/blob/master/LICENSE.md)\nCopyright (C) 2022 Isaac Beverly\n',
    'author': 'Isaac Beverly',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/imbev/pywebcanvas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
