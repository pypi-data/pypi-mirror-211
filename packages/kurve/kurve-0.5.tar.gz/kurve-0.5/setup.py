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



if __name__ == "__main__":

    setuptools.setup(
        name="kurve",
        version = 0.5,
        url="https://github.com/kurveai/kurve",
        packages = setuptools.find_packages(exclude=[ "docs", "examples" ]),
        install_requires = [
            "structlog >= 22.3.0",
            "dask >= 2023.1.1",
            "dask-sql >= 2023.2.0",
            "networkx >= 2.8.2",
            "pyvis >= 0.2.1",
            "psycopg2 >= 2.9.5",
            "pandas >= 1.4.2",
            "boto3 >= 1.24.12",
            "pyarrow >= 8.0.0",
            "awswrangler >= 2.18.0",
            "google-api-core==2.11.0",
            "google-auth==2.18.1",
            "google-cloud-bigquery==3.10.0",
            "google-cloud-core==2.3.2",
            "google-crc32c==1.5.0",
            "google-resumable-media==2.5.0",
            "googleapis-common-protos==1.59.0",
            "pydantic >= 1.10.5"
            ],
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
