# 0.0.1
from setuptools import setup, find_packages

VERSION = "0.0.1"

setup(
    name="PyBlingAPI",
    version=VERSION,
    author="Alexandre Defendi",
    author_email='alexandre_defendi@hotmail.com',
    keywords=['Bling'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(exclude=['*test*']),
    package_data={'pyblingapi': [
        'templates/*xml',
    ]},
    url='https://gitlab.com/Defendi/pyblingapi',
    license='LGPL-v2.1+',
    description='PyBlingAPI é uma biblioteca para troca de dados com o Bling ERP',
    long_description=open('README.md', 'r').read(),
    install_requires=[
        'requests==2.23.0',
    ],
    tests_require=[
        'pytest',
    ],
)
