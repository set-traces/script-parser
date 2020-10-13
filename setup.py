from setuptools import setup, find_packages

setup(
    name='script-parser',
    version='0.1.0',
    packages=find_packages(include=['script_parser', 'script_parser.*']),
    package_data={'script_parser': ['resources/*']}
)