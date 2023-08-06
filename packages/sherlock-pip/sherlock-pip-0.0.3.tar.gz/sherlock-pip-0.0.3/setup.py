import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sherlock-pip",
    version="0.0.3",
    author="Necrownyx",
    author_email="example@example.com",
    description="sherlock-project/sherlock as a command line application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Necrownyx/sherlock",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "certifi>=2019.6.16",
        "colorama>=0.4.1",
        "PySocks>=1.7.0",
        "requests>=2.22.0",
        "requests-futures>=1.0.0",
        "stem>=1.8.0 ",
        "torrequest>=0.1.0"
    ],
    package_dir={"": "src"},
    python_requires='>=3.6',
)