# -*- coding: utf-8 -*-
"""Installer for the redturtle.chefcookie package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="redturtle.chefcookie",
    version="2.1.0",
    description="Cookie policy integration with chefookie",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone",
    author="RedTurtle",
    author_email="info@redturtle.it",
    url="https://github.com/collective/redturtle.chefcookie",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/redturtle.chefcookie",
        "Source": "https://github.com/RedTurtle/redturtle.chefcookie",
        "Tracker": "https://github.com/RedTurtle/redturtle.chefcookie/issues",
    },
    python_requires=">=2.7",
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup", "node_modules"]),
    namespace_packages=["redturtle"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "plone.api",
        "BeautifulSoup4==4.9.3;python_version<'3'",
        "BeautifulSoup4>=4.9.3;python_version>='3'",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            "plone.testing>=5.0.0",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
