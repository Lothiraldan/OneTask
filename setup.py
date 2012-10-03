from distutils.core import setup

setup(
    name='OneTask',
    version='0.1dev',
    license='MIT License',
    long_description='Manage your tasks, one task at a time',
    requires=['pymongo'],
    scripts=['onetask']
)
