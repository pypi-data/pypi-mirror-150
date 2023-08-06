# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nessvec',
 'nessvec.data',
 'nessvec.data.constants',
 'nessvec.django_project',
 'nessvec.examples',
 'nessvec.examples.tbd',
 'nessvec.hist',
 'nessvec.scripts',
 'nessvec.wip']

package_data = \
{'': ['*'], 'nessvec.examples': ['ch06/.ipynb_checkpoints/*']}

install_requires = \
['ConfigArgParse==1.5.3',
 'Cython>=0.29.28',
 'beautifulsoup4==4.11.1',
 'boto3==1.22.2',
 'botocore==1.25.3',
 'django>=4.0,<5.0',
 'edit-distance==1.0.4',
 'elasticsearch==7.17.3',
 'environment==1.0.0',
 'gitpython>=3.1.27,<4.0.0',
 'graphviz>=0.20,<0.21',
 'h5py>=3.6.0,<4.0.0',
 'html2text>=2020.1.16,<2021.0.0',
 'html5lib==1.1',
 'jedi==0.18.1',
 'jupyter-client>=7.3.0',
 'jupyter-console>=6.4.2',
 'jupyter==1.0.0',
 'lxml==4.6.3',
 'm2r==0.2.1',
 'matplotlib-inline==0.1.3',
 'matplotlib==3.5.1',
 'meilisearch==0.18.2',
 'mistune==0.8.4',
 'pandas==1.1.3',
 'pillow==9.1.0',
 'pip>=22.0,<23.0',
 'poetry>=1.1.13',
 'pronouncing==0.2.0',
 'psutil>=5.8.0,<6.0.0',
 'python-dotenv>=0.13.0,<0.14.0',
 'python-slugify==4.0.0',
 'pyyaml==6.0',
 'rapidfuzz==0.9.1',
 'recommonmark==0.6.0',
 'scikit-image>=0.17.2,<0.18.0',
 'scikit-learn>=1.0,<2.0',
 'scipy==1.8.0',
 'seaborn>=0.11.2,<0.12.0',
 'sentence_transformers>=2.2.0,<3.0.0',
 'spacy==3.2.4',
 'torch==1.11.0',
 'tox>=3.25.0,<4.0.0',
 'tqdm>=4.60.0,<5.0.0',
 'wikipedia>=1.4.0,<2.0.0']

entry_points = \
{'console_scripts': ['nessvec = nessvec.main:main']}

setup_kwargs = {
    'name': 'nessvec',
    'version': '0.0.18',
    'description': "Decomposition of word embeddings (word vectors) into qualities ('ness'es).",
    'long_description': "# nessvec\n\n## Install from Source (recommended)\n\nClone the repository with all the source code and data:\n\n```console\n$ git clone git@gitlab.com:tangibleai/nessvec\n$ cd nessvec\n```\n\nCreate a conda environment and install the dependencies:\n\n```console\n$ conda create -n nessvec 'python==3.9.7'\n$ conda env update -n nessvec -f scripts/environment.yml\n$ pip install -e .\n```\n\n## Install from PyPi (only tested on Linux)\n\n```console\n$ pip install nessvec\n```\n\n## Get Started\n\n```python\n>>> from nessvec.util import load_glove\n>>> w2v = load_glove()\n>>> seattle = w2v['seattle']\n>>> seattle\narray([-2.7303e-01,  8.5872e-01,  1.3546e-01,  8.3849e-01, ...\n>>> portland = w2v['portland']\n>>> portland\narray([-0.78611  ,  1.2758   , -0.0036066,  0.54873  , -0.31474  ,...\n>>> len(portland)\n50\n>>> from numpy.linalg import norm\n>>> norm(portland)\n4.417...\n>>> portland.std()\n0.615...\n\n```\n\n```\n>>> cosine_similarity(seattle, portland)\n0.84...\n>>> cosine_similarity(portland, seattle)\n0.84...\n\n```\n\n```python\n>>> from nessvec.util import cosine_similarity\n>>> cosine_similarity(w2v['los_angeles'], w2v['mumbai'])\n.5\n\n```\n\n##\n\n",
    'author': 'Hobson Lane',
    'author_email': 'hobson@tangibleai.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/tangibleai/nessvec',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.3,<3.10.0',
}


setup(**setup_kwargs)
