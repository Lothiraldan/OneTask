from distutils.core import setup
from onetask import __version__

setup(
    name='OneTask',
    version=__version__,
    license='MIT License',
    long_description='Manage your tasks, one task at a time',
    requires=[],
    packages=['onetask'],
    scripts=['bin/onetask']
)
