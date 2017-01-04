from setuptools import setup

setup(
    name = "flatex",
    version = "0.1",
    extras_require = {
        'alternative-cli': 'Click',
        },
    entry_points='''
    [console_scripts]
    flatex=flatex:main
    ''',
)
