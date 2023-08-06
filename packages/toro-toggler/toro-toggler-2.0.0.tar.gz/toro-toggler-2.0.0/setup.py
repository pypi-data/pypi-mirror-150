import os

from setuptools import setup, find_packages

requires = []

setup(
    name='toro-toggler',
    version='2.0.0',
    description="TORO python markdown extension for wrapping image in special div tag",
    classifiers=[
        "Programming Language :: Python",
    ],
    author='Jerrick M. Pua',
    author_email='jerrick.pua@toro.io',
    keywords='python toro',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='toro-toggler',
    install_requires = requires,
)
