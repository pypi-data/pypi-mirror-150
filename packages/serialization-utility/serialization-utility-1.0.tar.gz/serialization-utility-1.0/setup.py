from codecs import open
from os import path

from setuptools import setup, find_packages

ROOT = path.abspath(path.dirname(__file__))

with open(path.join(ROOT, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="serialization-utility",
    version="1.0",
    description="serialization/deserialization of json/yaml/toml",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daniilandco",
    author="Daniil Bondarkov",
    author_email="daniilbondarcov@gmail.com",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["qtoml", "PyYAML", "setuptools"]
)
