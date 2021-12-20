from setuptools import setup

setup(
    name = "flatex",
    version = "0.1",
    install_requires = [
        'Click',
        ],
    py_modules=["flatex"],
    entry_points='''
    [console_scripts]
    flatex=flatex:main
    ''',
)
