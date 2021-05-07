from setuptools import setup
from pkg_resources import parse_requirements


with open("requirements.txt") as requirements_file:
    requirements = [str(req) for req in parse_requirements(
        requirements_file.readlines())]

setup(
    name="run",
    version="0.1",
    py_modules=["run"],
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        run=run:cli
    """,
)
