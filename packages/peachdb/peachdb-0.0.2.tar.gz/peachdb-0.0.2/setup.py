from pathlib import Path

from setuptools import find_packages, setup

requirements = []

# Read requirements from files
with open("requirements.txt", "r") as f:
    requirements.extend(f.read().splitlines())

# read the contents README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="peachdb",
    version="0.0.2",
    packages=find_packages(),
    install_requires=requirements,
    dependency_links=["https://download.pytorch.org/whl/cu113"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
