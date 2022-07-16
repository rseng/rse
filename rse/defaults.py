"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.logger import RSE_LOG_LEVEL
from rse.exceptions import MissingEnvironmentVariable
import logging
import multiprocessing
import os


logging.basicConfig(level=getattr(logging, RSE_LOG_LEVEL))
bot = logging.getLogger("rse.defaults")


def getenv(variable_key, default=None, required=False, silent=True):
    """attempt to get an environment variable. If the variable
    is not found, None is returned.

    Arguments:

     - variable_key (str) : the variable name
     - required (bool) : exit with error if not found
     - silent (bool) : Do not print debugging information
    """
    variable = os.environ.get(variable_key, default)
    if variable is None and required:
        raise MissingEnvironmentVariable(variable_key)

    if not silent and variable is not None:
        bot.debug("%s found as %s" % (variable_key, variable))

    return variable


RSE_NPROC = multiprocessing.cpu_count()
RSE_WORKERS = int(getenv("RSE_WORKERS", RSE_NPROC * 2 + 1))
RSE_SHELL = getenv("RSE_SHELL", "ipython")
RSE_CONFIG_FILE = getenv("RSE_CONFIG_FILE", "rse.ini")
RSE_CUSTOM_DATABASE_DIR = getenv("RSE_CUSTOM_DATABASE_DIR", "custom")

# Default database is filesystem
RSE_DATABASE = getenv("RSE_DATABASE")

# Database folder for filesystem or sqlite database
RSE_DATABASE_STRING = os.environ.get("RSE_DATABASE")

# Parsers installed
RSE_PARSERS = ["github"]

# Default taxonomy and criteria endpoints, and place to post annotation issues
RSE_API_ENDPOINT = getenv("RSE_API_ENDPOINT", "https://rseng.github.io/rseng/api")
RSE_ISSUE_ENDPOINT = getenv("RSE_ISSUE_ENDPOINT", "https://github.com/rseng/software")
RSE_HOST = getenv("RSE_HOST")
if RSE_HOST and RSE_HOST.endswith("/"):
    RSE_HOST = RSE_HOST.rstrip("/")

# MUST start and end with slash
RSE_URL_PREFIX = getenv("RSE_URL_PREFIX", "/")
if not RSE_URL_PREFIX.startswith("/"):
    RSE_URL_PREFIX = "/%s" % RSE_URL_PREFIX
if not RSE_URL_PREFIX.endswith("/"):
    RSE_URL_PREFIX = "%s/" % RSE_URL_PREFIX

# Dashboard settings
RSE_HOSTNAME = getenv("RSE_HOSTNAME", "127.0.0.1")
