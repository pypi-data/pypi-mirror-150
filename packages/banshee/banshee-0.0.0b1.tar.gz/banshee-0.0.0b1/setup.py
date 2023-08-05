# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['banshee', 'banshee.extra', 'banshee.middleware']

package_data = \
{'': ['*']}

install_requires = \
['exceptiongroup>=1.0.0-rc.3,<2.0.0']

extras_require = \
{'injector': ['injector>=0.19.0,<0.20.0']}

setup_kwargs = {
    'name': 'banshee',
    'version': '0.0.0b1',
    'description': '',
    'long_description': '# Banshee\n\n<p class="lead">\nA command dispatcher and message bus implementation for python.\n</p>\n\n## 🛠 Installing\n\n```\npoetry add banshee\n```\n\n## 📚 Help\n\nSee the [Documentation][docs] or ask questions on the [Discussion][discussions] board.\n\n## ⚖️ Licence\n\nThis project is licensed under the [MIT licence][mit_licence].\n\nAll documentation and images are licenced under the \n[Creative Commons Attribution-ShareAlike 4.0 International License][cc_by_sa].\n\n## 📝 Meta\n\nThis project uses [Semantic Versioning][semvar].\n\n[docs]: https://python-banshee.artisan.io\n[discussions]: https://github.com/artisanofcode/python-banshee/discussions\n[mit_licence]: http://dan.mit-license.org/\n[cc_by_sa]: https://creativecommons.org/licenses/by-sa/4.0/\n[semvar]: http://semver.org/',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
