import re
from pathlib import Path
import logging
import pkg_resources

log = logging.getLogger(__name__)


PKG_DIR = Path(__file__).absolute().resolve().parent
PKG_NAME = PKG_DIR.name
SRC_DIR = PKG_DIR.parent
REPO_DIR = SRC_DIR.parent
MANUSCRIPT_DIR = REPO_DIR.parent / 'nlpia-manuscript' / 'manuscript'
IMAGES_DIR = MANUSCRIPT_DIR / 'images'
ADOC_DIR = MANUSCRIPT_DIR / 'adoc'


def get_version():
    """ Look within setup.cfg for version = ... and within setup.py for __version__ = """
    version = '0.0.0'
    try:
        return pkg_resources.get_distribution(PKG_NAME)
    except Exception as e:
        log.error(e)
        log.warning(f"Unable to find {PKG_NAME} version so using {version}")
    return version

    # setup.cfg will not exist if package install in site-packages
    with (REPO_DIR / 'setup.cfg').open() as fin:
        for line in fin:
            matched = re.match(r'\s*version\s*=\s*([.0-9abrc])\b', line)
            if matched:
                return (matched.groups()[-1] or '').strip()


__version__ = get_version()

HOME_DIR = Path.home().resolve().absolute()
DATA_DIR_NAME = '.nlpia2-data'
DATA_DIR = PKG_DIR / DATA_DIR_NAME
if not DATA_DIR.is_dir():
    DATA_DIR = REPO_DIR / DATA_DIR_NAME
if not DATA_DIR.is_dir():
    DATA_DIR = HOME_DIR / DATA_DIR_NAME
    # try/except this and use tempfiles python module as backup
    DATA_DIR.mkdir(parents=True, exist_ok=True)

# canonical data directory to share data between nlpia2 installations
HOME_DATA_DIR = HOME_DIR / DATA_DIR_NAME
if not HOME_DATA_DIR.is_dir():
    HOME_DATA_DIR.mkdir(parents=True, exist_ok=True)

REPO_DATA_DIR, DATA_DIR = DATA_DIR, HOME_DATA_DIR

# DONE: create nlpia2/init.py
# DONE: add maybe_download() to init.py
# TODO: all required data files up to chapter07
# TODO: add list of all required data files to init.py
# TODO: ensure all files are in HOME_DATA_DIR (DATA_DIR is just a subset)
# TODO: move DATA_DIR constant to data.py
# DATA_FILENAMES = dict(
#     DATA_DIR
# )
