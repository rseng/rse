#!/usr/bin/env python

"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""


from setuptools import setup, find_packages
import os


def get_lookup():
    """get version by way of version file, returns a
    lookup dictionary with several global variables
    """
    lookup = dict()
    version_file = os.path.join("rse", "version.py")
    with open(version_file) as filey:
        exec(filey.read(), lookup)
    return lookup


def get_reqs(lookup=None, key="INSTALL_REQUIRES"):
    """get requirements, mean reading in requirements and versions from
    the lookup obtained with get_lookup
    """
    if lookup == None:
        lookup = get_lookup()

    install_requires = []
    for module in lookup[key]:
        module_name = module[0]
        module_meta = module[1]
        if "exact_version" in module_meta:
            dependency = "%s==%s" % (module_name, module_meta["exact_version"])
        elif "min_version" in module_meta:
            if module_meta["min_version"] == None:
                dependency = module_name
            else:
                dependency = "%s>=%s" % (module_name, module_meta["min_version"])
        install_requires.append(dependency)
    return install_requires


# Make sure everything is relative to setup.py
install_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(install_path)

# Get version information from the lookup
lookup = get_lookup()
VERSION = lookup["__version__"]
NAME = lookup["NAME"]
AUTHOR = lookup["AUTHOR"]
AUTHOR_EMAIL = lookup["AUTHOR_EMAIL"]
PACKAGE_URL = lookup["PACKAGE_URL"]
KEYWORDS = lookup["KEYWORDS"]
DESCRIPTION = lookup["DESCRIPTION"]
LICENSE = lookup["LICENSE"]
with open("README.md") as filey:
    LONG_DESCRIPTION = filey.read()

################################################################################
# MAIN #########################################################################
################################################################################

if __name__ == "__main__":

    INSTALL_REQUIRES = get_reqs(lookup)
    TESTS_REQUIRES = get_reqs(lookup, "TESTS_REQUIRES")
    ALL_REQUIRES = get_reqs(lookup, "ALL_REQUIRES")
    APP_REQUIRES = get_reqs(lookup, "APP_REQUIRES")
    DATABASE_REQUIRES = get_reqs(lookup, "DATABASE_REQUIRES")
    SCRAPER_REQUIRES = get_reqs(lookup, "SCRAPER_REQUIRES")

    setup(
        name=NAME,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=AUTHOR,
        maintainer_email=AUTHOR_EMAIL,
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        url=PACKAGE_URL,
        license=LICENSE,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        keywords=KEYWORDS,
        setup_requires=["pytest-runner"],
        install_requires=INSTALL_REQUIRES,
        tests_require=TESTS_REQUIRES,
        extras_require={
            "database": DATABASE_REQUIRES,
            "scraper": SCRAPER_REQUIRES,
            "app": APP_REQUIRES,
            "all": ALL_REQUIRES,
        },
        classifiers=[
            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
            "Topic :: Software Development",
            "Topic :: Scientific/Engineering",
            "Natural Language :: English",
            "Operating System :: Unix",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
        ],
        entry_points={"console_scripts": ["rse=rse.client:main"]},
    )
