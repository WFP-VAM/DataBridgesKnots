import os
from setuptools import setup, find_packages

# Get the long description from the README file
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='data_bridges_utils',
    version='1.0.0',
    description='Utilities for working with the WFP Data Bridges API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/your_org/data_bridges_utils',
    author='Your Name',
    author_email='your.email@example.com',
    license='AGPL 3.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='wfp data bridges api',
    packages=find_packages(exclude=['tests', 'tests.*']),
    python_requires='>=3.6',
    install_requires=[
        'PyYAML',
        'pandas>=2',
        'pystata',
        'stata-setup',
        'data_bridges_client',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'flake8',
            'black',
            'isort',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/your_org/data_bridges_utils/issues',
        'Source': 'https://github.com/your_org/data_bridges_utils',
    },
)