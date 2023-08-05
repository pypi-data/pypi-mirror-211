import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# upload pypi
# python setup.py sdist bdist_wheel
# twine upload dist/*

setup(
    name='nice-datapath',
    version='0.0.1',
    author='minusli',
    author_email='minusli@foxmail.com',
    url='https://github.com/minusli/nice-datapath',
    description='easy data picker',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests"]),
    python_requires='>=3',
    install_requires=[],
    entry_points={},
    license="Apache License 2.0"
)
