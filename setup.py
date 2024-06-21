import os
from setuptools import setup, find_packages

# Get the long description from the README file
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='data_bridges_knots',
    version='0.1.0',
    description='Wrapper for Data Bridges API client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/WFP-VAM/DataBridgesKnots',
    author='Alessandra Gherardelli, Valerio Giuffrida',
    author_email='alessandra.gherardelli@wfp.org, valerio.giuffrida@wfp.org',
    license='GNU General Public License v3 or later (GPLv3+)',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
    keywords=['VAM', 'WFP', 'data'],
    packages=find_packages(exclude=['tests', 'tests.*']),
    python_requires='>=3.9',
    extras_require={
        'dev': [
            'black',
            'bumpver',
            'isort',
            'pip-tools',
            'pytest',
        ],
        'data-bridges-utils': [],
        'data-bridges-utils-STATA': [
            'stata-setup',
            'pystata',
        ],
        'data-bridges-utils-R': [],
    },
)
