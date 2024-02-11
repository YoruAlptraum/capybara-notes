from setuptools import setup, find_packages

import py2exe

setup(
    windows=[{
        "script":"baseencoder.py",
        'dest_base': 'Capybara Notes',
        "icon_resources" : [(1, 'assets/capy-neon-closeup.ico')],
        'company_name': 'YoruAlptraum',
        'version': '1.3.0'
        }],
    options = {"py2exe": {
        "includes": {"tkinter"},
        'bundle_files': 1,
        'compressed': True
        }},
    packages=find_packages(exclude=['assets', 'config.json']),
    author="Ozawa | github.com/YoruAlptraum",
    description="Simple mds app",
)