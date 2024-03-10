from setuptools import setup, find_packages

import py2exe

setup(
    windows=[{
        "script":"baseencoder.py",
        'dest_base': 'Capybara Notes',
        "icon_resources" : [(1, 'assets/capy-neon-closeup.ico')],
        'company_name': 'YoruAlptraum',
        'version': '1.4.1'
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

# configuration for using nuitka 
# nuitka --standalone --output-dir=%userprofile%\downloads --enable-plugin=tk-inter --remove-output --disable-console --windows-icon-from-ico=assets/capy-neon-closeup.ico --output-filename="Capybara Notes" --company-name=YoruAlptraum --product-name=Capybara_Notes --file-version=1.4.1 --product-version=1.4.1 --file-description="Simple mds app" mdsApp.py 
