import sys
from subprocess import CalledProcessError, check_call

from setuptools import setup

try:
    check_call([sys.executable, '-m', 'pip', 'install', 'cuvec'])
except CalledProcessError:
    setup()
else:
    setup(install_requires=['cuvec'])
