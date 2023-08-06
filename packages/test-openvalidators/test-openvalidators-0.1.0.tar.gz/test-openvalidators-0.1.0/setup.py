import pathlib
import pkg_resources
from setuptools import setup


def read(fname):
    this_directory = pathlib.Path(__file__).parent
    long_description = (this_directory / fname).read_text()
    return long_description


def read_requirements(path):
    with pathlib.Path(path).open() as requirements_txt:
        return [
            str(requirement)
            for requirement in pkg_resources.parse_requirements(requirements_txt)
        ]


requirements = read_requirements("requirements.txt")

VERSION = "0.1.0"

setup(
    name="test-openvalidators",
    version=VERSION,
    description="Openvalidators is a collection of open source validators for the Bittensor Network.",
    url="https://github.com/opentensor/foundation_validator",  # TODO: add repo url
    author="bittensor.com",
    packages=["openvalidators"],
    include_package_data=True,
    author_email="",
    license="MIT",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": ["foundation-validator = openvalidators.neuron:main"],
    },
    install_requires=requirements,
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    maintainer="",
    maintainer_email="",
    keywords=[
        "bittensor",
        "validator",
        "ai",
        "machine-learning",
        "deep-learning",
        "blockchain",
        "pytorch",
        "torch",
        "neural-networks",
        "cryptocurrency",
    ],
)
