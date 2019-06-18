from setuptools import setup

setup(
    name="ml-enabler-cli",
    version='0.1.0',
    py_modules=['ml_enabler'],
    install_requires=[
        'Click',
        'numpy',
        'mercantile==1.0.4',
        'aiohttp==3.5.4',
        'backoff==1.8.0',
        'pytest==4.6.3',
        'Shapely==1.6.4.post2',
        'area==1.1.1',
        '-e git+git@github.com:hotosm/ml-enabler-cli.git@d44686d69fee2ca9fa78a5857c64cb6ba194c3b5#egg=ml_enabler_cli'
    ],
    entry_points='''
        [console_scripts]
        ml-enabler=ml_enabler.cli:main_group
    ''',
)
