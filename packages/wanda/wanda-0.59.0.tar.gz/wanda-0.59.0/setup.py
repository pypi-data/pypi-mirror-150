# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wanda']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0',
 'cloudscraper>=1.2.60,<2.0.0',
 'colorthief>=0.2.1,<0.3.0',
 'filetype>=1.0.13,<2.0.0',
 'lxml>=4.8.0,<5.0.0',
 'musicbrainzngs>=0.7.1,<0.8.0',
 'screeninfo>=0.8,<0.9']

entry_points = \
{'console_scripts': ['wanda = wanda.wanda:run']}

setup_kwargs = {
    'name': 'wanda',
    'version': '0.59.0',
    'description': 'Set wallpapers with keywords or randomly',
    'long_description': '# wanda\nScript to set wallpaper using keyword or randomly\n\n![Codacy branch grade](https://img.shields.io/codacy/grade/e5aacd529ce04f3fb8c0f9ce6a3bdd9e/main)\n![PyPI](https://img.shields.io/pypi/v/wanda)\n![PyPI - Downloads](https://img.shields.io/pypi/dw/wanda)\n![PyPI - License](https://img.shields.io/pypi/l/wanda)\n![Gitlab code coverage](https://img.shields.io/gitlab/coverage/kshib/wanda/main)\n![Gitlab pipeline](https://img.shields.io/gitlab/pipeline-status/kshib/wanda?branch=main)\n\n## Installation\n```\npip install wanda\n```\nor `pip install -i https://test.pypi.org/simple/ wanda` for dev version\n\n## Usage\n```\nwanda\nwanda -t mountain\nwanda -s wallhaven -t japan\n```\n`wanda -h` for more details\n\n## Notes\n- By default the source is [unsplash](https://unsplash.com).\n- Some sources may have inapt images. Use them at your own risk.\n\n## Supported sources\n\n- [4chan](https://boards.4chan.org)\n- [500px](https://500px.com)\n- [artstation](https://artstation.com)\n- [imgur](https://imgur.com)\n- local\n- [reddit](https://reddit.com)\n- [unsplash](https://unsplash.com)\n- [wallhaven](https://wallhaven.cc)\n\n# Demo\n- [Desktop, Manjaro Linux](https://z.zz.fo/om26p.webm)\n\n## Automate\n* To set wallpaper at regular intervals automatically:\n\n0. Install (for android only):\n```\ntermux-wake-lock\npkg in cronie termux-services nano\nsv-enable crond\n```\n1. Edit crontab\n```\ncrontab -e\n```\n2. Set your desired interval. For hourly:\n```\n@hourly wanda -t mountains\n```\n[(more examples)](https://crontab.guru/examples.html)\n\n4. ctrl+o to save, ctrl+x to exit the editor\n\n## Build\n[python](https://www.python.org/downloads/) and [poetry](https://python-poetry.org/) are needed\n```\ngit clone https://gitlab.com/kshib/wanda.git && cd wanda\npoetry build\n```\n\n## Uninstall\n```\npip uninstall wanda\n```\n\n## Shell\nOlder versions can be found [here (android)](https://gitlab.com/kshib/wanda/-/tree/sh-android) and [here (desktop)](https://gitlab.com/kshib/wanda/-/tree/sh-desktop)\nThey support [canvas](https://github.com/adi1090x/canvas/blob/master/canvas) and [earthview](https://earthview.withgoogle.com/) as source which have not yet been added to python version.\n\n## Issues\nThere might be issues with certain sources or platforms.\nFor now, the script is only tested on Manjaro+KDE and Android+Termux\nFeel free to raise issues if you encounter them.\n\n## License\nMIT\n',
    'author': 'kshib',
    'author_email': 'ksyko@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/kshib/wanda',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
