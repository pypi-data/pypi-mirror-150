# nlpia2

<!-- [![PyPI version](https://img.shields.io/pypi/pyversions/nlpia2.svg)](https://pypi.org/project/nlpia2/)
 [![License](https://img.shields.io/pypi/l/qary.svg)](https://pypi.python.org/pypi/qary/)
 -->
<!-- https://gitlab.com/username/userproject/badges/master/coverage.svg
 -->
[![codecov](https://codecov.io/gl/tangibleai/nlpia2/branch/master/graph/badge.svg)](https://codecov.io/gl/tangibleai/nlpia2)
[![GitLab CI](https://gitlab.com/tangibleai/nlpia2/badges/master/pipeline.svg)](https://gitlab.com/tangibleai/nlpia2/badges/master/pipeline.svg)



Official code repository for the book [_Natural Language Processing in Action, 2nd Edition_](https://proai.org/nlpia2e) by Maria Dyshel and Hobson Lane at [Tangible AI](https://tangibleai.com). It would not have happened without the generous work of [contributing authors](AUTHORS.md) and prosocial AI developers.

To get the most of this repository, you need to do two things.

1. **Clone the repository** to your local machine if you want to execute the code locally or want local access to the data (recommended).
2. **Create an environment** that has all the helpful/needed modules for Natural Language Processing In Action, 2nd Edition.

## Clone the Repository

If you're currently viewing this file on gitlab, and want in the future to access the data and code local to your machine, you may clone this repository to your local machine. Navigate to your preferred directory to house the local clone (for example, you local _git_ directory) and execute:

`git clone git@gitlab.com:prosocialai/nlpia2`

## Create a Conda Environment

To use the various packages in vogue with today's advanced NLP referenced in the NLPIA 2nd Edition book, such as PyTorch and SpaCy, you need to install them in a conda environment.  To avoid potential conflics of such packages and their dependencies with your other python projects, it is a good practice to create and activate a _new_ conda environment.

Here's how we did that for this book.

1. **Make sure you have Anaconda3 installed.** Make sure you can run conda from within a bash shell (terminal). The `conda --version` command should say something like '`4.10.3`.

2. **Update conda itself**. Keep current the `conda` package, which manages all other packages. Your base environment is most likely called _base_ so you can execute `conda update -n base -c defaults conda` to bring that package up to date.  Even if _base_ is not the activated environment at the moment, this command as presented will update the conda package in the _base_ environment. This way, next time you use the `conda` command, in any environment, the system will use the updated _conda_ package.

3. **Create a new environment and install the variety of modules needed in NLPIA 2nd Edition.**

There are two ways to do that.  

### Use the script already provided in the repository (_`nlpia2/src/nlpia2/scripts/conda_install.sh`_)

If you have cloned the repository, as instructed above, you already have a script that will do this work. From the directory housing the repository, run
`cd nlpia2/src/nlpia2/scripts/` and from there run `bash conda_install.sh` 

### Or manually execute portions of the script as follows

First, create a new environment (or activate it if it exists)

```bash
# create a new environment named "nlpia2" if one doesn't already exist:
conda activate nlpia2 \
    || conda create -n nlpia2 -y 'python==3.9.7' \
    && conda activate nlpia2
```

Once that completes, install all of `nlpia2`'s conda dependences if they aren't already installed:

``` bash
conda install -c defaults -c huggingface -c pytorch -c conda-forge -y \
    emoji \
    ffmpeg \
    glcontext \
    graphviz \
    huggingface_hub \
    jupyter \
    lxml \
    manimpango \
    nltk \
    pyglet \
    pylatex \
    pyrr \
    pyopengl \
    pytest \
    pytorch \
    regex \
    seaborn \
    scipy \
    scikit-learn \
    sentence-transformers \
    statsmodels \
    spacy \
    torchtext \
    transformers \
    wikipedia \
    xmltodict
```

Finally, install via pip any packages not available through conda channels.  In such scenarios it is generally a better practice to apply all pip installs after _all_ conda installs.  Furthermore, to ensure the pip installation is properly configured for the python version used in the conda environment, rather than use `pip` or `pip3`, activate the environment and invoke pip by using `python -m pip`.

``` bash
conda activate nlpia2
python -m pip install manim manimgl
```

## Ready, Set, Go!

Congratulations! You now have the nlpia2 repository cloned which gives you local access to all the data and scripts need in the NLPIA Second Edition book, and you have created a powerful environment to use.  When you're ready to type or execute code, check if this environment is activated. If not, activate by executing:

`conda activate nlpia2`

And off you go tackle some serious Natural Language Processing, in order to make the world a better place for all.

Run a jupyter notebook server within docker:
`jupyter-repo2docker --editable .`
