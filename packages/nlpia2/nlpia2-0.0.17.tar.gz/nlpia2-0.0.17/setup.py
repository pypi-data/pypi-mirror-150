# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nlpia2',
 'nlpia2.bonus',
 'nlpia2.bonus.ipython-sessions',
 'nlpia2.ch01',
 'nlpia2.ch02',
 'nlpia2.ch03',
 'nlpia2.ch04',
 'nlpia2.ch05',
 'nlpia2.ch06',
 'nlpia2.ch07',
 'nlpia2.ch07.cnn',
 'nlpia2.ch07.cnn.cnn',
 'nlpia2.ch08',
 'nlpia2.ch12',
 'nlpia2.ch12.inc',
 'nlpia2.ch12.inc.flashtext',
 'nlpia2.ch12.inc.preprocessing',
 'nlpia2.etl',
 'nlpia2.first-edition',
 'nlpia2.pug',
 'nlpia2.review_questions',
 'nlpia2.scripts',
 'nlpia2.unused']

package_data = \
{'': ['*'],
 'nlpia2.ch05': ['.ipynb_checkpoints/*'],
 'nlpia2.ch06': ['.ipynb_checkpoints/*'],
 'nlpia2.ch07.cnn': ['data/*'],
 'nlpia2.ch12.inc.preprocessing': ['json/*']}

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
 'pip==22.0.4',
 'pronouncing==0.2.0',
 'psutil>=5.8.0,<6.0.0',
 'python-dotenv>=0.13.0,<0.14.0',
 'python-slugify==4.0.0',
 'pyyaml==6.0',
 'qary>=0.7,<0.8',
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
 'wikipedia>=1.4,<2.0']

entry_points = \
{'console_scripts': ['cnn = ch07.cnn.main']}

setup_kwargs = {
    'name': 'nlpia2',
    'version': '0.0.17',
    'description': 'Natural language processing utilities and examples for the book Natural Language Processing in Action (nlpia) 2nd Edition by Hobson Lane and Maria Dyshel.',
    'long_description': '# nlpia2\n\n<!-- [![PyPI version](https://img.shields.io/pypi/pyversions/nlpia2.svg)](https://pypi.org/project/nlpia2/)\n [![License](https://img.shields.io/pypi/l/qary.svg)](https://pypi.python.org/pypi/qary/)\n -->\n<!-- https://gitlab.com/username/userproject/badges/master/coverage.svg\n -->\n[![codecov](https://codecov.io/gl/tangibleai/nlpia2/branch/master/graph/badge.svg)](https://codecov.io/gl/tangibleai/nlpia2)\n[![GitLab CI](https://gitlab.com/tangibleai/nlpia2/badges/master/pipeline.svg)](https://gitlab.com/tangibleai/nlpia2/badges/master/pipeline.svg)\n\n\n\nOfficial code repository for the book [_Natural Language Processing in Action, 2nd Edition_](https://proai.org/nlpia2e) by Maria Dyshel and Hobson Lane at [Tangible AI](https://tangibleai.com). It would not have happened without the generous work of [contributing authors](AUTHORS.md) and prosocial AI developers.\n\nTo get the most of this repository, you need to do two things.\n\n1. **Clone the repository** to your local machine if you want to execute the code locally or want local access to the data (recommended).\n2. **Create an environment** that has all the helpful/needed modules for Natural Language Processing In Action, 2nd Edition.\n\n## Clone the Repository\n\nIf you\'re currently viewing this file on gitlab, and want in the future to access the data and code local to your machine, you may clone this repository to your local machine. Navigate to your preferred directory to house the local clone (for example, you local _git_ directory) and execute:\n\n`git clone git@gitlab.com:prosocialai/nlpia2`\n\n## Create a Conda Environment\n\nTo use the various packages in vogue with today\'s advanced NLP referenced in the NLPIA 2nd Edition book, such as PyTorch and SpaCy, you need to install them in a conda environment.  To avoid potential conflics of such packages and their dependencies with your other python projects, it is a good practice to create and activate a _new_ conda environment.\n\nHere\'s how we did that for this book.\n\n1. **Make sure you have Anaconda3 installed.** Make sure you can run conda from within a bash shell (terminal). The `conda --version` command should say something like \'`4.10.3`.\n\n2. **Update conda itself**. Keep current the `conda` package, which manages all other packages. Your base environment is most likely called _base_ so you can execute `conda update -n base -c defaults conda` to bring that package up to date.  Even if _base_ is not the activated environment at the moment, this command as presented will update the conda package in the _base_ environment. This way, next time you use the `conda` command, in any environment, the system will use the updated _conda_ package.\n\n3. **Create a new environment and install the variety of modules needed in NLPIA 2nd Edition.**\n\nThere are two ways to do that.  \n\n### Use the script already provided in the repository (_`nlpia2/src/nlpia2/scripts/conda_install.sh`_)\n\nIf you have cloned the repository, as instructed above, you already have a script that will do this work. From the directory housing the repository, run\n`cd nlpia2/src/nlpia2/scripts/` and from there run `bash conda_install.sh` \n\n### Or manually execute portions of the script as follows\n\nFirst, create a new environment (or activate it if it exists)\n\n```bash\n# create a new environment named "nlpia2" if one doesn\'t already exist:\nconda activate nlpia2 \\\n    || conda create -n nlpia2 -y \'python==3.9.7\' \\\n    && conda activate nlpia2\n```\n\nOnce that completes, install all of `nlpia2`\'s conda dependences if they aren\'t already installed:\n\n``` bash\nconda install -c defaults -c huggingface -c pytorch -c conda-forge -y \\\n    emoji \\\n    ffmpeg \\\n    glcontext \\\n    graphviz \\\n    huggingface_hub \\\n    jupyter \\\n    lxml \\\n    manimpango \\\n    nltk \\\n    pyglet \\\n    pylatex \\\n    pyrr \\\n    pyopengl \\\n    pytest \\\n    pytorch \\\n    regex \\\n    seaborn \\\n    scipy \\\n    scikit-learn \\\n    sentence-transformers \\\n    statsmodels \\\n    spacy \\\n    torchtext \\\n    transformers \\\n    wikipedia \\\n    xmltodict\n```\n\nFinally, install via pip any packages not available through conda channels.  In such scenarios it is generally a better practice to apply all pip installs after _all_ conda installs.  Furthermore, to ensure the pip installation is properly configured for the python version used in the conda environment, rather than use `pip` or `pip3`, activate the environment and invoke pip by using `python -m pip`.\n\n``` bash\nconda activate nlpia2\npython -m pip install manim manimgl\n```\n\n## Ready, Set, Go!\n\nCongratulations! You now have the nlpia2 repository cloned which gives you local access to all the data and scripts need in the NLPIA Second Edition book, and you have created a powerful environment to use.  When you\'re ready to type or execute code, check if this environment is activated. If not, activate by executing:\n\n`conda activate nlpia2`\n\nAnd off you go tackle some serious Natural Language Processing, in order to make the world a better place for all.\n\nRun a jupyter notebook server within docker:\n`jupyter-repo2docker --editable .`\n',
    'author': 'Hobson Lane',
    'author_email': 'hobson@tangibleai.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://proai.org',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.3,<3.10.0',
}


setup(**setup_kwargs)
