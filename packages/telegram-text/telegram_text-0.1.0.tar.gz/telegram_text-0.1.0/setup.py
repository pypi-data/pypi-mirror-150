# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegram_text']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'telegram-text',
    'version': '0.1.0',
    'description': 'Python markup module for Telegram messenger. This module provides a rich list of components to build any possible markup fast and render it to specific html or MarkdownV2 formats.',
    'long_description': '# telegram-text\n**Python markup module for Telegram messenger.\nThis module provides a rich list of components to build any possible\nmarkup fast and render it to specific _html_ and _MarkdownV2_ formats.**\n\n[![versions](https://img.shields.io/pypi/pyversions/telegram-text.svg)](https://github.com/SKY-ALIN/telegram-text)\n![Tests](https://github.com/SKY-ALIN/telegram-text/actions/workflows/tests.yml/badge.svg)\n![Code Quality](https://github.com/SKY-ALIN/telegram-text/actions/workflows/code-quality.yml/badge.svg)\n[![codecov](https://codecov.io/gh/SKY-ALIN/telegram-text/branch/dev/graph/badge.svg?token=BK0ASC89B9)](https://codecov.io/gh/SKY-ALIN/telegram-text)\n[![PyPI version fury.io](https://badge.fury.io/py/telegram-text.svg)](https://pypi.org/project/telegram-text/)\n[![license](https://img.shields.io/github/license/SKY-ALIN/telegram-text.svg)](https://github.com/SKY-ALIN/telegram-text/blob/main/LICENSE)\n\n---\n\n### Installation\nInstall using `pip install telegram-text` or `poetry add telegram-text`\n\n### Basic Example\n\n```python\nfrom telegram_text import Bold, Italic, Underline\n\ntext = Underline(Bold("Bold") + "and" + Italic("italic") + "with underline.")\n```\n\n<p align="center">\n  <img \n    width="400"\n    src="https://raw.githubusercontent.com/SKY-ALIN/telegram-text/dev/docs/source/_static/basic_example_result.jpg"\n  />\n</p>\n\n### Advanced Example\n\n```python\nfrom telegram_text import Bold, Chain, Italic, TOMLSection, Hashtag, Link, UnorderedList\n\ndescription = "A Channel about software developing and distributing. Subscribe to follow new technologies."\ntags: dict[str, str] = {...}  # Tags description with following format `tag: tag_description`\nlinks: dict[str, str] = {...}  # Links with following format `text: url`\n\nmenu = Chain(\n    TOMLSection(\n        \'Menu\',\n        Italic(description),\n    ),\n    TOMLSection(\n        \'Tags\',\n        *[Hashtag(tag, style=Bold) + f"- {about}" for tag, about in tags.items()],\n    ),\n    TOMLSection(\n        \'Links\',\n        UnorderedList(*[Link(text, url) for text, url in links.items()]),\n    ),\n    sep=\'\\n\\n\'\n)\n```\n\n![Advanced Example Result](https://raw.githubusercontent.com/SKY-ALIN/telegram-text/dev/docs/source/_static/advanced_example_result.jpg)\n\n---\n\nFull documentation and reference are available at \n[telegram-text.alinsky.tech](https://telegram-text.alinsky.tech)',
    'author': 'Vladimir Alinsky',
    'author_email': 'Vladimir@Alinsky.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://telegram-text.alinsky.tech',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
