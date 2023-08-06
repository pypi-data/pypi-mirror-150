# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dane', 'dane.handlers']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch7>=7.17.3,<8.0.0', 'pika>=1.2.1,<2.0.0', 'yacs>=0.1.8,<0.2.0']

setup_kwargs = {
    'name': 'dane',
    'version': '0.3.1',
    'description': 'Utils for working with the Distributed Annotation and Enrichment system',
    'long_description': "# DANE\nThe Distributed Annotation 'n' Enrichment (DANE) system handles compute task assignment and file storage for the automatic annotation of content.\n\nThis repository contains contains the building blocks for with DANE, such as creating custom analysis workers or submitting new task.\n\n## Installation\n\nThis package can be installed through pip:\n\n    pip install dane\n\n### Configuration\n\nDANE components are configured through the DANE.config module, which is described here: https://dane.readthedocs.io/en/latest/intro.html#configuration \nIt is however noteable that, because all DANE components are expected to rely on it, some of the DANE-server, ElasticSearch and RabbitMQ configuration \nare included in the default config. As such it is recommended that you create a `$HOME/.dane/config.yml` or `$DANE_HOME/config.yml` which contain machine-wide settings for how to connect to these services, which involves specifying the following settings:\n\n```\nDANE:\n    API_URL: 'http://localhost:5500/DANE/'\n    MANAGE_URL: 'http://localhost:5500/manage/'\nRABBITMQ:\n    HOST: 'localhost'\n    PORT: 5672\n    EXCHANGE: 'DANE-exchange'\n    RESPONSE_QUEUE: 'DANE-response-queue'\n    USER: 'guest'\n    PASSWORD: 'guest'\nELASTICSEARCH:\n    HOST: ['localhost']\n    PORT: 9200\n    USER: 'elastic'\n    PASSWORD: 'changeme'\n    SCHEME: 'http'\n```\n\nThe values given here are the default values.\n\n### Usage\n\nExamples of how to use DANE can be found in the `examples/` directory.\n",
    'author': 'Nanne van Noord',
    'author_email': 'n.j.e.vannoord@uva.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CLARIAH/DANE',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
