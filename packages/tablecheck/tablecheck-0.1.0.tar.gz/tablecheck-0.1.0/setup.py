from setuptools import setup

setup(
    name="tablecheck",
    version="0.1.0",
    description="A minimalistic framework for verifying criteria that has been logged across multiple sheets.",
    url="https://www.github.com/ryanbaekr/tablecheck",
    author="Ryan Baker",
    license="AGPL",
    packages=["tablecheck"],
    python_requires=">=3.6",
    install_requires=["pandas",
                      "openpyxl",
                      ],

    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
    ],
)
