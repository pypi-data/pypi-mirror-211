from setuptools import setup
from pathlib import Path

setup(
    name='cmdsave',
    version='1.0.3',
    readme="README.md",
    description="💾 CMDs",
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=['cmdsave'],
    install_requires=[
        'argparse',
        'tabulate',
        'keyboard',
        'pyperclip',
    ],
    entry_points={
        'console_scripts': [
            'cmds = cmdsave.cmdsave:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: Microsoft :: Windows",
    ],
    platforms=['Windows'],
    repository='https://github.com/lenzfliker/cmdsave',
    keywords=[
        'save',
        'cli',
        'console',
        'terminal',
        'prductivity',]
)
