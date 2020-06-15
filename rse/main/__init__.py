"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main.config import Config
from rse.defaults import RSE_DATABASE, RSE_PARSERS, RSE_CONFIG_FILE

from rse.exceptions import RepoNotFoundError
from rse.main.database import init_db
from rse.utils.prompt import confirm
from rse.utils.file import read_file
from rse.main.parsers import get_parser
from rse.main.criteria import get_criteria
from rse.main.taxonomy import get_taxonomy

import logging
import os
import re

bot = logging.getLogger("rse.main")
parser_regex = "github"


class Encyclopedia:
    """An encyclopedia is one or more namespaces to store research
       software. By default, we create a structure on the filesystem,
       however an sqlite database (or other) can be used.
    """

    def __init__(self, config_file=None, database=None, generate=False):
        """create a software repository. We take a config file, which should
           sit at the root of the repository, and then parse the subfolders
           accordingly.
        """
        self.config = Config(config_file or RSE_CONFIG_FILE, generate=generate)
        self.config_dir = os.path.dirname(self.config.configfile)
        self.initdb(database)

    def initdb(self, database):
        """setup the rse home (where the config directory is stored) and the
           database specification. If a database string is required (and not
           provided) alert the user and exit on error).

           Arguments:
            - config_dir (str) : the configuration directory (home for rse)
            - database (str) : a string to specify the database setup
        """
        self.database = (
            database
            or RSE_DATABASE
            or self.config.get("DEFAULT", "database")
            or "filesystem"
        )
        database_string = self.config.get("DEFAULT", "databaseconnect")
        bot.info("Database: %s" % self.database)

        # Supported database options
        valid = ("sqlite", "postgresql", "mysql+pymysql", "filesystem")
        if not self.database.startswith(valid):
            bot.warning(
                "%s is not yet a supported type, saving to filesystem." % self.database
            )
            self.database = "filesystem"

        # Create database client with functions for database type
        self.db = init_db(
            self.database,
            config_dir=self.config_dir,
            database_string=database_string,
            config=self.config,
        )

    def exists(self, uid):
        """based on a parser type and unique identifier, determine if software
           exists in the database
        """
        parser = get_parser(uid, config=self.config)
        return self.db.exists(parser.uid)

    def list(self, name=None):
        """A wrapper to the database list_repos function. Optionally take
           a whole parser name (e.g., github) or just a specific uid. No
           parser indicates that we list everything.
        """
        return self.db.list_repos(name)

    def list_criteria(self):
        """Get a listing of criteria from the rse API
        """
        if not hasattr(self, "criteria"):
            self.criteria = get_criteria()
        return self.criteria

    def list_taxonomy(self):
        """Get a listing of a flattened taxonomy from the rse API
        """
        if not hasattr(self, "taxonomy"):
            self.taxonomy = get_taxonomy()
        return self.taxonomy

    def bulk_add(self, filename):
        """Given a filename with a single list of repos, add each
        """
        repos = []
        if os.path.exists(filename):
            for name in read_file(filename):
                uid = name.strip()
                repos += [self.add(uid, quiet=True)] or []
        return repos

    def bulk_update(self, filename):
        """Given a filename with a single list of repos, add each
        """
        repos = []
        if os.path.exists(filename):
            for name in read_file(filename):
                uid = name.strip()
                try:
                    repos += [self.update(uid)]
                except RepoNotFoundError:
                    pass
        return repos

    def add(self, uid, quiet=False):
        """A wrapper to add a repository to the software database.
        """
        if not self.exists(uid):
            repo = self.db.add(uid)
            return repo
        if not quiet:
            bot.error(f"{uid} already exists in the database.")

    def get(self, uid=None):
        """A wrapper to get a repo id from the database. If an id is not provided,
           will return the last updated repo based on timestamp of file or database.
        """
        return self.db.get(uid)

    def get_or_create(self, uid):
        return self.db.get_or_create(uid)

    def clear(self, target=None, noprompt=False):
        """clear takes a target, and that can be a uid, parser, or none
           We ask the user for confirmation.
        """
        # Case 1: no target indicates clearing all
        if not target:
            if noprompt or confirm(
                "This will delete all software in the database, are you sure?"
            ):
                return self.db.clear()

        # Case 2: it's a parser
        elif target in RSE_PARSERS:
            if noprompt or confirm(
                f"This will delete all {target} software in the database, are you sure?"
            ):
                return self.db.delete_parser(target)

        # Case 3, it's a specific software identifier
        elif re.search(parser_regex, target):
            if noprompt or confirm(
                f"This will delete software {target}, are you sure?"
            ):
                return self.db.delete_repo(target)

        else:
            raise RuntimeError(f"Unrecognized {target} to clear")

    def update(self, uid):
        """Update an existing software repository.
        """
        try:
            repo = self.get(uid)
            self.db.update(repo)
            bot.info(f"{repo.uid} has been updated.")
            return repo
        except RepoNotFoundError:
            bot.error(f"{uid} does not exist.")

    def search(self, query):
        """Search across commands and general metadata for a string of interest.
           We use regular expressions (re.search) so they are supported.
           Search is only available for non-filesystem databases.
        """
        results = self.db.search(query)
        if results:
            return results
        bot.info(f"No results matching {query}")
