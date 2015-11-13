from setuptools import setup

setup(
    name = "flatex",
    version = "0.1",
    install_requires = [
        'Click',
        ],
    entry_points='''
    [console_scripts]
    flatex=flatex:main
    ''',
)
