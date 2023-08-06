# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gummy', 'gummy.cli', 'gummy.utils']

package_data = \
{'': ['*'], 'gummy': ['templates/*', 'templates/components/*']}

install_requires = \
['Jinja2>=3.1.1,<4.0.0',
 'MarkupSafe>=2.0.1,<3.0.0',
 'PyPDF2>=1.27.3,<2.0.0',
 'Werkzeug>=1.0.1,<2.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'html5lib>=1.1,<2.0',
 'lxml>=4.6.3,<5.0.0',
 'nltk>=3.6.2,<4.0.0',
 'pdfkit>=0.6.1,<0.7.0',
 'pdfminer>=20191125,<20191126',
 'pylatexenc>=2.10,<3.0',
 'python-dotenv>=0.17.1,<0.18.0',
 'python-magic>=0.4.22,<0.5.0',
 'requests>=2.27.1,<3.0.0',
 'selenium>=4.1.3,<5.0.0',
 'undetected-chromedriver>=3.1.5,<4.0.0']

entry_points = \
{'console_scripts': ['gummy-driver = gummy.cli.check_driver:check_driver',
                     'gummy-journal = '
                     'gummy.cli.translate_journal:translate_journal',
                     'gummy-translate = '
                     'gummy.cli.translate_text:translate_text']}

setup_kwargs = {
    'name': 'translation-gummy',
    'version': '4.0.1',
    'description': 'Translation Gummy is a magical gadget which enables user to be able to speak and understand other languages.',
    'long_description': '# Translation-Gummy\n\n![header](https://github.com/iwasakishuto/Translation-Gummy/blob/master/image/header.png?raw=true)\n[![PyPI version](https://badge.fury.io/py/Translation-Gummy.svg)](https://pypi.org/project/Translation-Gummy/)\n[![GitHub version](https://badge.fury.io/gh/iwasakishuto%2FTranslation-Gummy.svg)](https://github.com/iwasakishuto/Translation-Gummy)\n[![Execute Translation-Gummy](https://github.com/iwasakishuto/Translation-Gummy/workflows/Execute%20Translation-Gummy/badge.svg)](https://github.com/iwasakishuto/Translation-Gummy/blob/master/.github/workflows/execute_python_package.yml)\n[![Upload to PyPI](https://github.com/iwasakishuto/Translation-Gummy/workflows/Upload%20to%20PyPI/badge.svg)](https://github.com/iwasakishuto/Translation-Gummy/blob/master/.github/workflows/upload_python_package.yml)\n[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/iwasakishuto/Translation-Gummy/blob/master/LICENSE)\n[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/iwasakishuto/Translation-Gummy/blob/master/examples/Colaboratory.ipynb)\n[![Docker file](https://img.shields.io/badge/%F0%9F%90%B3-Dockerfile-0db7ed?style=flat-radius)](https://github.com/iwasakishuto/Translation-Gummy/blob/master/docker/Dockerfile)\n[![Documentation](https://img.shields.io/badge/Documentation-portfolio-001d34?style=flat-radius)](https://iwasakishuto.github.io/Translation-Gummy/index.html)\n[![twitter badge](https://img.shields.io/badge/twitter-Requests-1da1f2?style=flat-radius&logo=twitter)](https://www.twitter.com/messages/compose?recipient_id=1042783905697288193&text=Please%20support%20this%20journal%3A%20)\n[![Qiita badge1](https://img.shields.io/badge/「ほん訳コンニャク」を食べて論文を読もう-Qiita-64c914?style=flat-radius)](https://qiita.com/cabernet_rock/items/670d5cd597bcd9f2ff3f)\n[![Qiita badge2](https://img.shields.io/badge/「ほん訳コンニャク」を使ってみよう。-Qiita-64c914?style=flat-radius)](https://qiita.com/cabernet_rock/items/1f9bff5e0b9363da312d)\n[![website](https://img.shields.io/badge/website-Translation--Gummy-lightblue)](https://elb.translation-gummy.com/)\n[![Sponsor](https://img.shields.io/badge/%E2%9D%A4-Sponsor-db61a2)](https://github.com/sponsors/iwasakishuto)\n[![Add to Slack](https://platform.slack-edge.com/img/add_to_slack.png)](https://elb.translation-gummy.com/slack_auth_begin)\n\n**Translation Gummy** is a **_magical gadget_** which enables user to be able to speak and understand other languages. **※ Supported journals are listed [here](https://github.com/iwasakishuto/Translation-Gummy/wiki/Supported-journals).**\n\n## Installation\n\n1. Install **`Translation-Gummy`** (There are two ways to install):\n    - **Install from PyPI (recommended):**\n        ```sh\n        $ sudo pip install Translation-Gummy\n        ```\n   - **Alternatively: install `Translation-Gummy` from the GitHub source:**\n       ```sh\n       $ git clone https://github.com/iwasakishuto/Translation-Gummy.git\n       # If you want to use the latest version (under development)\n       $ git clone -b develop https://github.com/iwasakishuto/Translation-Gummy.git\n       $ cd Translation-Gummy\n       $ sudo python setup.py install\n       ```\n2. Install **`wkhtmltopdf`**\n   - **Debian/Ubuntu:**\n        ```sh\n        $ sudo apt-get install wkhtmltopdf\n        ```\n    - **macOS:**\n        ```sh\n        $ brew install homebrew/cask/wkhtmltopdf\n        ```\n3. Install **driver** for `selenium`:\n**`Selenium`** requires a driver to interface with the chosen browser, so please visit the [documentation](https://selenium-python.readthedocs.io/installation.html#drivers) to install it.\n    ```sh\n    # Example: Chrome\n    # visit "chrome://settings/help" to check your chrome version.\n    # visit "https://chromedriver.chromium.org/downloads" to check <Suitable.Driver.Version> for your chrome.\n    $ wget https://chromedriver.storage.googleapis.com/<Suitable.Driver.Version>/chromedriver_mac64.zip\n    $ unzip chromedriver_mac64.zip\n    $ mv chromedriver /usr/local/bin/chromedriver\n    $ chmod +x /usr/local/bin/chromedriver\n    ```\n\n※ See [![Docker file](https://img.shields.io/badge/%F0%9F%90%B3-Dockerfile-0db7ed?style=flat-radius)](https://github.com/iwasakishuto/Translation-Gummy/blob/master/docker/Dockerfile) or [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/iwasakishuto/Translation-Gummy/blob/master/examples/Colaboratory.ipynb) for more specific example.\n\n### Pyenv + Poetry\n\n- [Pyenv](https://github.com/pyenv/pyenv) is a python installation manager.\n- [Poetry](https://python-poetry.org/) is a packaging and dependency manager.\n\nI recommend you to use these tools to **avoid the chaos** of the python environment. See other sites for how to install these tools.\n\n```sh\n$ pyenv install 3.8.9\n$ pyenv local 3.8.9\n$ python -V\nPython 3.8.9\n# For Windows\n$ poetry install -E windows\n# For the other platform\n$ poetry install\n$ poetry run gummy-translate "This is a pen." --from-lang en --to-lang ja\n$ poetry run gummy-journal "https://www.nature.com/articles/ncb0800_500"\n```\n\n## Quick example\n\n- **[example notebooks](https://nbviewer.jupyter.org/github/iwasakishuto/Translation-Gummy/blob/master/examples/)**\n- **Translation**:\n    - **Python Module:**\n    ```python\n    >>> from gummy import TranslationGummy\n    >>> model = TranslationGummy(translator="deepl", from_lang="en", to_lang="ja")\n    [success] local driver can be built.\n    [failure] remote driver can\'t be built.\n    DRIVER_TYPE: local\n    >>> model.en2ja("This is a pen.")\n    DeepLTranslator (query1) 02/30[#-------------------]  6.67% - 2.144[s]   translated: これはペン\n    \'これはペンです。\'\n    ```\n    - **Command line:**\n    ```sh\n    $ gummy-translate "This is a pen." --from-lang en --to-lang ja\n    [success] local driver can be built.\n    [failure] remote driver can\'t be built.\n    DRIVER_TYPE: local\n    DeepLTranslator (query1) 02/30[#-------------------]  6.67% - 2.185[s]   translated: これはペン\n    これはペンです。\n    ```\n    - **Output**\n    ![gummy-translate](https://github.com/iwasakishuto/Translation-Gummy/blob/master/image/demo.gummy-translate.gif?raw=true)\n- **Create PDF (with translation)**\n    - **Python Module:**\n    ```python\n    >>> from gummy import TranslationGummy\n    >>> model = TranslationGummy(gateway="utokyo", translator="deepl")\n    >>> pdfpath = model.toPDF(url="https://www.nature.com/articles/ncb0800_500", delete_html=True)\n    ```\n    - **Command line:**\n    ```sh\n    $ gummy-journal "https://www.nature.com/articles/ncb0800_500"\n    ```\n    - **Output**\n    ![gummy-journal](https://github.com/iwasakishuto/Translation-Gummy/blob/master/image/demo.gummy-journal.gif?raw=true)\n\n\n',
    'author': 'iwasakishuto',
    'author_email': 'cabernet.rock@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://iwasakishuto.github.io/Translation-Gummy/index.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
