import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="simple_sugar",
    version="1.0.0",
    description="Syntactic sugar for beginners!",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jmoseley99/simple_sugar",
    author="Jacob Moseley",
    author_email="jm01295@surrey.ac.uk",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
)