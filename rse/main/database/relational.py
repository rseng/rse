"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.exceptions import (
    MissingDatabaseString,
    NoReposError,
    MultipleReposExistError,
    RepoNotFoundError,
)
from rse.main.database.base import Database
from rse.main.parsers import get_parser
from rse.main.parsers.base import ParserBase
from rse.utils.strings import update_nonempty

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import or_

import logging
import json

bot = logging.getLogger("rse.main.database.relational")


class RelationalDatabase(Database):
    """
    A RelationalDatabase is a more robust relational datbase (to sqlite).
    Since the global database property can be any of postgresql, mysql+pysq;,
    it is defined on init. The sqlite database also uses this class, but defines
    a custom init function to handle the rse.db file.
    """

    def __init__(self, config_dir, config=None, **kwargs):
        """
        init for the filesystem ensures that the base folder (named
        according to the studyid) exists.
        """
        self.database = kwargs.get("database")
        self.config = config
        database_string = kwargs.get("database_string")
        if not database_string:
            raise MissingDatabaseString

        # The database url includes the type and string
        self.db = "%s://%s" % (self.database, database_string)
        self.create_database()

    def create_database(self):
        """
        create the databsae based on the string, whether it's relational or
        sqlite. self.db must be defined.
        """
        from rse.main.database.models import Base

        self.engine = create_engine(self.db)
        self.session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )
        Base.query = self.session.query_property()
        Base.metadata.create_all(bind=self.engine)
        self.Base = Base

    # Global

    def exists(self, uid):
        """
        Determine if a repo exists.
        """
        from rse.main.database.models import SoftwareRepository

        parser = get_parser(uid, config=self.config)
        repo = SoftwareRepository.query.filter(
            SoftwareRepository.uid == parser.uid
        ).first()
        return repo is not None

    def get_or_create(self, uid):
        """
        Determine if a repo exists.
        """
        from rse.main.database.models import SoftwareRepository

        parser = get_parser(uid, config=self.config)
        repo = SoftwareRepository.query.filter(
            SoftwareRepository.uid == parser.uid
        ).first()
        if not repo:
            repo = self.add(uid)
        return repo

    def clear(self):
        """
        clear (delete) all repos. This could be improved to cascade instead.
        """
        from rse.main.database.models import SoftwareRepository

        SoftwareRepository.query.delete()
        self.session.commit()
        return True

    # Add or Update requires executor

    def add(self, uid, data=None):
        """
        Create a new repo based on a uid that matches to a parser.
        """
        from rse.main.database.models import SoftwareRepository

        parser = get_parser(uid, config=self.config)
        if not self.exists(parser.uid):

            if not data:
                data = parser.get_metadata()
            else:
                parser.data = data

            # If it's a parser handoff
            if isinstance(data, ParserBase):
                parser = data
                data = parser.data

            if data:
                repo = SoftwareRepository(
                    uid=parser.uid, parser=parser.name, data=json.dumps(parser.export())
                )
                self.session.add(repo)
                self.session.commit()
                bot.info(f"{parser.uid} was added to the the database.")
                repo.parser = parser
                return repo

    def update(self, repo, updates=None, rewrite=False, data=None):
        """
        update a repo with a json dictionary.
        """
        # Return of None indicates non-success
        data = data or repo.parser.get_metadata()
        if data:
            updates = updates or {}
            updates.update(repo.parser.export())

            # Load the previous data to update
            data = {}
            if repo.data and not rewrite:
                data = json.loads(repo.data)
            if "data" in data:
                data["data"] = update_nonempty(updates, data["data"])
            else:
                data = update_nonempty(updates, data)
            repo.data = json.dumps(data)
            self.session.add(repo)
            self.session.commit()
            return repo

    def label(self, repo, key, value, force=False):
        """
        Update a repository with a specific key/value pair.
        """
        data = {}
        if repo.data:
            data = json.loads(repo.data)

        if key in data and not force:
            raise RuntimeError(
                f"{key} is already defined for {repo.uid}. Use --force to overwrite."
            )
        data.update({key: value})
        bot.debug(f"Adding key {key}:{value}")
        repo.data = json.dumps(data)
        self.session.add(repo)
        self.session.commit()
        return repo

    # Get, delete, etc. only require uid

    def get(self, uid=None):
        """
        Get a repo based on a uid. Exits on error if doesn't exist. If
        a uid is not provided, get the last updated repository.
        """
        from rse.main.database.models import SoftwareRepository

        # Retrieve either the last repo, or the one with a specific uid
        if not uid:
            repo = (
                self.session.query(SoftwareRepository)
                .order_by(desc("timestamp"))
                .first()
            )
            parser = get_parser(repo.uid, config=self.config)
            if not repo:
                raise NoReposError
        else:
            parser = get_parser(uid, config=self.config)
            repo = SoftwareRepository.query.filter(
                SoftwareRepository.uid == parser.uid
            ).first()

            # If an exact match isn't there, look for partial match
            if not repo:
                query = "%" + parser.uid + "%"
                query = self.session.query(SoftwareRepository).filter(
                    SoftwareRepository.uid.ilike(query)
                )
                results = self.session.execute(query).fetchall()
                if len(results) == 1:
                    return self.get(results[0][0])
                elif len(results) > 1:
                    raise MultipleReposExistError(parser.uid)
                else:
                    raise RepoNotFoundError(parser.uid)

        repo.parser = parser
        return repo

    def delete_repo(self, uid):
        """
        delete a repo based on a specific repo id.
        """
        from rse.main.database.models import SoftwareRepository

        repo = self.get(uid)
        if not repo:
            bot.error(f"{uid} does not exist in the database.")
            return False
        SoftwareRepository.query.filter(SoftwareRepository.uid == repo.uid).delete()
        self.session.commit()
        bot.info(f"{uid} has been removed.")
        return True

    def delete_parser(self, name):
        """
        delete all repos for a parser, based on parser's name (str).
        """
        from rse.main.database.models import SoftwareRepository

        deleted_items = False
        for repo in SoftwareRepository.query.filter(
            SoftwareRepository.parser_name == name
        ):
            deleted_items = True
            self.session.delete(repo)
        self.session.commit()
        return deleted_items

    def list_repos(self, name=None):
        """
        list repos, either under a particular parser name (if provided)
        or just the parsers.
        """
        from rse.main.database.models import SoftwareRepository

        if name:
            repos = SoftwareRepository.query.filter(
                SoftwareRepository.parser_name == name
            )
        else:
            repos = SoftwareRepository.query.all()

        rows = []
        for repo in repos:
            rows.append([repo.uid])
        return rows

    def search(self, query, taxonomy=None, criteria=None):
        """
        Search across the database for a particular query.
        """
        from rse.main.database.models import SoftwareRepository

        # We will return a lookup of results
        results = {}

        # Required to have a query
        if not query:
            return results

        # Ensure that query can be part of a larger string
        expression = "%" + query + "%"

        result = self.session.query(SoftwareRepository).filter(
            or_(
                SoftwareRepository.data.ilike(expression),
                SoftwareRepository.uid.ilike(expression),
            )
        )
        # list of tuples, (uid, datetime, executor]
        results = self.session.execute(result).fetchall()
        return {query: [[r[0], str(r[2]), str(r[1])] for r in results]}
