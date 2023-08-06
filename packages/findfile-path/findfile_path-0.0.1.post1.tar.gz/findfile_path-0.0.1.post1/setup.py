#! /usr/bin/env python

from setuptools import setup, find_packages
import versioneer

setup (
    name = "findfile_path",
    version = versioneer.get_version (),
    description = "Find file on path with optional extensions",
    long_description = open ("README.rst").read (),
    cmdclass = versioneer.get_cmdclass (),
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: "
        + "GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Utilities",
    ],
    keywords = "find_file search_file",
    author = "J C Lawrence",
    author_email = "claw@kanga.nu",
    url = "https://github.com/clearclaw/findfile_path",
    license = "LGPL v3.0",
    test_suite = "tests", 
    packages = find_packages (exclude = ["tests",]),
    package_data = {
    },
    zip_safe = True,
    install_requires = [line.strip ()
        for line in open ("requirements.txt").readlines ()],
    entry_points = {
        "console_scripts": [
        ],
    },
)
