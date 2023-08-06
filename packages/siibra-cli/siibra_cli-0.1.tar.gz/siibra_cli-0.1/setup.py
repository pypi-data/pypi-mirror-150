from setuptools import setup, find_packages
import os
import re

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def find_version():
    path_to_init = os.path.join(ROOT_DIR, "siibra_cli/__init__.py")
    with open(path_to_init, "r", encoding="utf-8") as f:
        content = f.read()
        version_match = re.search(r"^__version__ *= *['\"](.*?)['\"]$", content, re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("siibra-cli version cannot be found.")


with open(os.path.join(ROOT_DIR, "README.rst"), "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="siibra_cli",
    version=find_version(),
    author="Big Data Analytics Group, Forschungszentrum Juelich, Institute of Neuroscience and Medicine (INM-1)",
    author_email="inm1-bda@fz-juelich.de",
    description="Basic commandline client for siibra - a software toolsuite for interacting with brain atlases",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/FZJ-INM1-BDA/siibra-cli",
    packages=find_packages(include=["siibra_cli"]),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    entry_points="""
        [console_scripts]
        siibra=siibra_cli.cli:siibra
    """,
    python_requires=">=3.7",
    install_requires=[
        "siibra>=0.3a16",
        "click>=8.0",
        "click-plugins>=1.0",
        "simple-term-menu>=1.4",
    ],
)
