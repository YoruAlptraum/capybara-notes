from setuptools import setup, find_packages

import py2exe

setup(
    windows=[{
        "script":"mdsApp.py",
        "icon_resources" : [(1, 'assets/capy-neon-closeup.ico')]
        }],
    options = {"py2exe": {
        "includes": {"tkinter"},
        'bundle_files': 1,
        'compressed': True
        }},
    packages=find_packages(include=['assets', 'config.json']),
    author="Ozawa | github.com/YoruAlptraum",
    description="Simple mds app",
    version="1.1.0",
)