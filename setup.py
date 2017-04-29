from setuptools import find_packages
from setuptools import setup


PACKAGE_NAME = 'repo_monitor'


setup(
    name=PACKAGE_NAME,
    version='0.1.0',
    description='Utility for monitoring certain aspects of a repo',
    author='Michael Christen',
    url='https://github.com/michael-christen/repo-monitor',
    license='MIT',
    packages=find_packages(exclude=["*.tests"]),
    install_requires=[
    ],
    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': ['repomon=repo_monitor.parser:main'],
    },
)
