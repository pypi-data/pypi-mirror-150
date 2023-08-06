#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="gpn_zsdparser",
    version= "1.1",
    author="Anatoly Bryksin",
    author_email="anatoly.bryksin@gmail.com",
    description="",
    use_scm_version={"root": "..", "relative_to": __file__},
    setup_requires=[""],
    install_requires=[
        "kaitaistruct==0.9",
        "psycopg2-binary==2.9.1",
        "SQLAlchemy==1.4.22",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
)
