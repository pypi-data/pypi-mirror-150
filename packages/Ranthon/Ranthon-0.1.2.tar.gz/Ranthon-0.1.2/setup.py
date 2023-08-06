from setuptools import setup

__project__  = "Ranthon"
__version__ = "0.1.2"
__description__ = "a bunch of random python modules"
__packages__ = ["infseq"]
__requires__ = ["filelog"]

setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    requires = __requires__
)
