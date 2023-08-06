import importlib.util
import pathlib
import setuptools
import typing


KEYWORDS = [
    "knowledge discovery",
    "data discovery",
    "data visualization",
    "entity linking",
    "graph algorithms",
    "knowledge graph",
    "parsing",
    ]


def parse_requirements_file (filename: str) -> typing.List:
    """read and parse a Python `requirements.txt` file, returning as a list of str"""
    results: list = []

    with pathlib.Path(filename).open() as f:
        for l in f.readlines():
            results.append(l.strip().replace(" ", "").split("#")[0])

    return results


if __name__ == "__main__":
    base_packages = parse_requirements_file("requirements.txt")

    setuptools.setup(
        name="kurve",
        version = 0.4,
        url="https://github.com/kurveai/kurve",
        packages = setuptools.find_packages(exclude=[ "docs", "examples" ]),
        package_data={'kurve':['requirements.txt']},
        install_requires = base_packages,
        extras_require = {
            "base": base_packages
            },

        author="Wes Madrigal",
        author_email="wes@madconsulting.ai",
        license="MIT",

        description="An interface for dynamic entity linking with graphs as the backend for arbitrary data sources.",
        long_description = pathlib.Path("README.md").read_text(),
        long_description_content_type = "text/markdown",

        keywords = ", ".join(KEYWORDS),
        classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Information Technology",
            "Intended Audience :: Science/Research",
            "Topic :: Scientific/Engineering :: Information Analysis",
            ],

        project_urls = {
            "Source" : "http://github.com/kurveai/kurve",
            "Issue Tracker" : "https://github.com/kurveai/kurve/issues"
            },

        zip_safe=False,
        )
