import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="numjpy",
    version="4.0.0",
    description="NUMPY",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="SWAMINARAYAN",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    packages=["numjpy"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "numjpy=numjpy.__main__:main",
        ]
    },
)