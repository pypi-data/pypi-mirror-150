from setuptools import setup, find_packages

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="MySerializers",
    version="1.2",
    description="library for python serialization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArtemDemba/LabsPython/tree/master",
    author="Dembovskiy Artem",
    author_email="DVL.45@mail.com",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent"
    ],
    packages=["MySerializers/json", "MySerializers/src", "MySerializers/toml", "MySerializers/yaml"],
    include_package_data=True
)
