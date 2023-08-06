from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent

__project__  = "Ranthon"
__version__ = "0.1.5"
__description__ = "a bunch of random python modules"
__packages__ = ["infseq"]
__requires__ = ["filelog"]
__long_description__ = (this_directory / "README.md").read_text()
__long_description_content_type__ = 'text/markdown'

setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    requires = __requires__,
    long_description = __long_description__,
    long_description_content_type = __long_description_content_type__
)
