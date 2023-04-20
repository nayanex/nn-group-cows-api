import os
from configparser import RawConfigParser

from setuptools import find_packages, setup


def parse_requirements(filename):
    """Load requirements from a pip requirements file"""
    return [
        line.strip()
        for line in open(filename)
        if line and not (line.strip().startswith("#") or line.strip().startswith("--"))
    ]


REQUIRES = parse_requirements("./requirements/requirements.txt")

TEST_REQUIRES = parse_requirements("./requirements/requirements-test.txt")

RELEASE_REQUIRES = ["bump2version", "wheel", "twine"]

bumpversion_config = RawConfigParser()
if os.path.exists(".bumpversion.cfg"):
    bumpversion_config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".bumpversion.cfg"))
else:
    bumpversion_config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), "bumpversion.cfg"))

setup(
    name="cow_api",
    version=bumpversion_config.get("bumpversion", "current_version"),
    description="COW API",
    author="Nayana",
    author_email="holanda.nayana@gmail.com",
    package_dir={"": "cow-api/src"},
    packages=find_packages("src"),
    install_requires=REQUIRES,
    extras_require={"test": TEST_REQUIRES, "release": RELEASE_REQUIRES, "mssql": ["pyodbc!=4.0.32"]},
)
