from setuptools import setup, find_packages
from pkg_resources import parse_requirements

with open("requirements.txt") as requirements_file:
    requirements = [
        str(req) for req in parse_requirements(requirements_file.readlines())
    ]

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()


setup(
    name="github_metrics",
    version="0.0.4",
    description="Generate development metrics using github data for your project.",
    url="https://github.com/vintasoftware/github-metrics",
    author="Victoria Pantoja (Vinta Software)",
    author_email="victoria.pantoja@vinta.com.br",
    python_requires=">=3.8",
    py_modules=["github_metrics"],
    install_requires=requirements,
    include_package_data=True,
    packages=find_packages(include=["github_metrics", "github_metrics.*"]),
    entry_points="""
        [console_scripts]
        github_metrics=github_metrics.run:cli
    """,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
)
