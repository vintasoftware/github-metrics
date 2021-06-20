from setuptools import setup
from pkg_resources import parse_requirements


with open("requirements.txt") as requirements_file:
    requirements = [
        str(req) for req in parse_requirements(requirements_file.readlines())
    ]

setup(
    name="github_metrics",
    version="0.1",
    python_requires=">=3.8",
    py_modules=["github_metrics"],
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        github_metrics=github_metrics.run:cli
    """,
)
