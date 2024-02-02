from setuptools import setup, find_packages

import py2exe

setup(
    windows=[{
        "script":"mdsApp.py",
        "icon_resources" : [(1, 'assets/capy neon.ico')]
        }],
    options = {"py2exe": {
        "includes": {"tkinter"},
        'bundle_files':1,
        'compressed': True
        }},
    packages=find_packages(include=['assets', 'config.json']),
)