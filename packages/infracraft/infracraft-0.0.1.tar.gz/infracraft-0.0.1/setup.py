from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Module for automating the creation of project infrastructure in the cloud'
LONG_DESCRIPTION = 'This module allows you to automate the creation of infrastructure in the Yandex Cloud using a configuration file.'

setup(
    name='infracraft',
    version=VERSION,
    author='Sv',
    author_email='cvity6692@gmail.com',
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'cloud', 'infrastructure']
)