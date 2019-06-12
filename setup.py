import re
from setuptools import setup

version = re.search(r"^__version__\s*=\s*'(.*)'", open('cachalyze/cachalyze.py').read(), re.M).group(1)

with open('README.md', 'rb') as f:
    long_descr = f.read().decode('utf-8')

setup(
    name='cachalyze',
    packages=['cachalyze'],
    entry_points={
        'console_scripts': ['cachalyze = cachalyze.cachalyze:main']
    },
    version=version,
    description='Cache sensitivity analyzer for C/C++ programs.',
    long_description=long_descr,
    author='Dennis Johannes Spaan',
    author_email='dennis@spaan.io',
    url='',
)
