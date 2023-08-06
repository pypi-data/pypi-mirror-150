"""H&A Geotechnical Design and Python Library (GTL), 2022.

Strictly for internal use.
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hagtl",
    version="0.0.1b",
    author="Haley & Aldrich, Inc.",
    author_email="nmachairas@haleyaldrich.com",
    description="H&A Geotechnical Design and Python Library (GTL)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.haleyaldrich.com/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where="hagtl"),
    python_requires=">=3.8",
)
