"""
pyjeopardy
----------

pyJeopardy is a Python implementation of the Jeopardy game that supports
an Arduino based buzzer system.
"""
from setuptools import setup

from pyjeopardy.version import VERSION


setup(
    name='pyjeopardy',
    version=VERSION,
    license='GPLv3',
    author='Sven Hertle',
    author_email='hertle@fs.tum.dee',
    description='A Python implementation of the Jeopardy game.',
    long_description=__doc__,
    zip_safe=False,
    include_package_data=True,
    platforms='UNIX',
    setup_requires=[],
    install_requires=[
        'pyqt5',
        'pyserial'
    ],
    scripts=[
        'run-pyjeopardy'
    ],
    packages=['pyjeopardy'],
    py_modules=['pyjeopardy'],
    package_dir={'pyjeopardy': 'pyjeopardy'},
)
