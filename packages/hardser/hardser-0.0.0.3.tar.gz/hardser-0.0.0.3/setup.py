from setuptools import find_packages, setup

setup(
    name="hardser",
    version="0.0.0.3",
    author="Mikhail Hancharou",
    author_email="engeneer2003@mail.ru",
    packages=find_packages(include=['modules', 'modules.*']),
    entry_points={
        'console_scripts': [
            'hardser=Converter:setup',  # modules.converter:setup
        ],
    },
    install_requires=[
        'coverage==6.3.2',
        'entrypoints==0.3',
        # 'py==1.10.0',
        'pytest==7.1.2',
        'pytest-cov==3.0.0',
        # 'python-apt==2.0.6+ubuntu0.20.04.3',
        'PyYAML==5.3.1',
        'simplejson==3.16.0',
        'toml==0.10.2',
        'virtualenv==20.0.17',
    ]
)