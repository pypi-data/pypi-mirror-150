from pathlib import Path

from setuptools import setup, find_packages

from src import asyncspawner


setup(
    name='AsyncSpawner',
    version=asyncspawner.__version__,
    description='Spawn asyncio coroutines over threads running in multiple processes.',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    author='Konstantin Tolstikhin',
    author_email='k.tolstikhin@gmail.com',
    url='https://github.com/ktolstikhin/asyncspawner',
    bugtrack_url='https://github.com/ktolstikhin/asyncspawner/issues',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.7',
    install_requires=[],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
    zip_safe=False,
)
