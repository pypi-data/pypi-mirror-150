from setuptools import setup, find_packages

setup(
    name="hardser",
    version="0.0.2.0",
    author="Mikhail Hancharou",
    author_email="engeneer2003@mail.ru",
    packages=find_packages(),  # ['modules', 'Converter']
    entry_points={
        'console_scripts': ['hardser=Converter.Converter:setup'],
    },
    install_requires=[
        'coverage==6.3.2',
        'entrypoints==0.3',
        'pytest==7.1.2',
        'pytest-cov==3.0.0',
        'PyYAML==5.3.1',
        'simplejson==3.16.0',
        'toml==0.10.2',
        'virtualenv==20.0.17',
    ]
)
