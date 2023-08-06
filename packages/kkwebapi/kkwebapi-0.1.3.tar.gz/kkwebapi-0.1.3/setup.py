# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kkwebapi']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.0,<2.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'kkwebapi',
    'version': '0.1.3',
    'description': 'Web API wrapper for Koikatu / EmotionCreators official uploader.',
    'long_description': '# KoikatuWebAPI\nA Web API wrapper for Koikatu / EmotionCreators official uploader.\n\n# Installation\nThis module is available on [PyPI](https://pypi.org/project/kkwebapi/).\n```\n$ pip install kkwebapi\n```\n```\n$ python -m pip install kkwebapi\n```\n\n# Basic Usage\n```python\n>>> from kkwebapi import KoikatuWebAPI\n>>> df = KoikatuWebAPI.get_ranking()\n>>> print(df)\n          id  sex  height  bust  hair  personality  blood_type  ...    name  nickname handle_name            comment download_num                                                uid  weekly_download_num\n0          1    1       1     2     2            0           3  ...   高岡 結香        ユイ    ILLUSION       ILLUSIONサンプル         1256  gOuAD02g92pX05r3Sj2aJJeJ01FdWqh01pe5PM1284vK01...                    6\n...\n```',
    'author': 'great-majority',
    'author_email': 'yosaku.ideal+github@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/great-majority/KoikatuWebAPI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
