from setuptools import setup

import api_limit


def readme():
    '''Read README file'''
    with open('README.md') as infile:
        return infile.read()


setup(
    name='api_limit',
    version="v0.0.2",
    description='API rate limit decorator',
    long_description=readme().strip(),
    long_description_content_type='text/markdown',
    packages=['api_limit'],
    install_requires=[],
    include_package_data=True,
    zip_safe=False
)
