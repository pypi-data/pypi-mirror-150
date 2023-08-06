# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['travel_map', 'travel_map.scripts']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pyecharts>=1.9.1,<2.0.0']

extras_require = \
{'docs': ['mike>=1.1.2,<2.0.0',
          'mkdocs>=1.3.0,<2.0.0',
          'mkdocs-material>=8.2.13,<9.0.0',
          'mkdocstrings-python-legacy>=0.2.2,<0.3.0'],
 'test': ['pytest>=7.1.2,<8.0.0', 'pytest-cov>=3.0.0,<4.0.0']}

entry_points = \
{'console_scripts': ['travel-map = travel_map.scripts.commands:travel_map']}

setup_kwargs = {
    'name': 'travel-map',
    'version': '2.0.0',
    'description': 'A tool to generate travel map.',
    'long_description': '# 旅行地图\n\n这是一个精确到城市旅行地图生成器。\n本项目是基于开源项目 [pyechart](https://github.com/pyecharts/pyecharts)，\n生成的中国地图符合法律规范。\n\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/hktkzyx/travel-map/Build%20and%20Test%20Python%20Package)\n![Codecov](https://img.shields.io/codecov/c/github/hktkzyx/travel-map)\n![PyPI](https://img.shields.io/pypi/v/travel-map)\n![PyPI - License](https://img.shields.io/pypi/l/travel-map)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/travel-map)\n![GitHub last commit](https://img.shields.io/github/last-commit/hktkzyx/travel-map)\n\n## 安装\n\n```bash\npip install travel-map\n```\n\n## 使用\n\n用户需要将旅行信息输入到一个 CSV 文件里，例如\n\n```csv travelled_cities.csv\n城市,组\n北京,旅行\n上海,旅行\n武汉,居住\n香港,中转\n```\n\n文件中城市的名称可以查阅[文件](https://github.com/pyecharts/pyecharts/blob/d1b2ecd223b6c6d429e698ec690e15bf8c40ae09/pyecharts/datasets/map_filename.json)。\n\n然后运行命令\n\n```bash\ntravel-map --title "我的旅行地图" --output travel_map.html travelled_cities.csv\n```\n\n即可生成标题为`我的旅行地图`的精确到城市的旅行地图如下\n\n![demo](./demo/demo.png)\n\n## 如何贡献\n\n十分欢迎 Fork 本项目！\n欢迎修复 bug 或开发新功能。\n开发时请遵循以下步骤:\n\n1. 使用 [poetry](https://python-poetry.org/) 作为依赖管理\n\n    克隆项目后，在项目文件夹运行\n\n    ```bash\n    poetry install\n    ```\n\n2. 使用 [pre-commit](https://pre-commit.com/) 并遵守 [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) 规范\n\n    安装 pre-commit 并运行\n\n    ```bash\n    pre-commit install -t pre-commit -t commit-msg\n    ```\n\n    建议使用 [commitizen](https://github.com/commitizen-tools/commitizen) 提交您的 commits。\n\n3. 遵循 [gitflow](https://nvie.com/posts/a-successful-git-branching-model/) 分支管理策略\n\n    安装 [git-flow](https://github.com/petervanderdoes/gitflow-avh) 管理您的分支并运行\n\n    ```bash\n    git config gitflow.branch.master main\n    git config gitflow.prefix.versiontag v\n    git flow init -d\n    ```\n\n4. PR 代码到 develop 分支\n\n## 许可证\n\n木兰宽松许可证，第2版 （Mulan Permissive Software License，Version 2）\n\nCopyright (c) 2019 hktkzyx\n\ntravel-map is licensed under Mulan PSL v2.\n\nYou can use this software according to the terms and conditions of the Mulan PSL v2.\n\nYou may obtain a copy of Mulan PSL v2 at: <http://license.coscl.org.cn/MulanPSL2>\n\nTHIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,\nEITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,\nMERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.\n\nSee the Mulan PSL v2 for more details.\n',
    'author': 'hktkzyx',
    'author_email': 'hktkzyx@yeah.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hktkzyx/travel-map',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
