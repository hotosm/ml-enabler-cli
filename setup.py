from setuptools import setup

setup(
    name="ml-enabler-cli",
    version='0.1.0',
    py_modules=['ml_enabler'],
    install_requires=[
        'Click',
        'mercantile==1.0.4',
        'aiohttp==3.5.4'
    ],
    entry_points='''
        [console_scripts]
        ml-enabler=ml_enabler.cli:main_group
    ''',
)
