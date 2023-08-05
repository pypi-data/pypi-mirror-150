import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="data-eng-helper",
    version="1.0.0",
    description="data engineers helper module",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/omusana/dataeng_exercise/tree/master/exercise_2",
    author="Oscar Musana Asiimwe",
    author_email="omusana@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True
)
