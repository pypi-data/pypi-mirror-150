import os
from setuptools import setup

def read(filename):
    current_directory = os.path.dirname(__file__)
    filepath = os.path.join(current_directory, filename)
    with open(filepath) as f:
        return f.read()

setup(
    name="polimap",
    version="0.0.1",
    author="Jon Moss",
    author_email="me@jonathanmoss.me",
    url="https://github.com/maclover7/polimap",
    description="Political mapping, made easy.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=("polimap",),
    entry_points={"console_scripts": ("polimap = polimap")},
    install_requires=[],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="election"
)
