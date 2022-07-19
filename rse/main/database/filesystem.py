"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.exceptions import (
    DirectoryNotFoundError,
    MultipleReposExistError,
    RepoNotFoundError,
    NoReposError,
)
from rse.utils.file import (
    write_json,
    write_file,
    mkdir_p,
    read_json,
    read_file,
    recursive_find,
    get_latest_modified,
)
from rse.main.database.base import Database
from rse.main.parsers import get_parser
from rse.main.parsers.base import ParserBase
from rse.utils.strings import update_nonempty
from glob import glob
import logging
import shutil
import os
import re

bot = logging.getLogger("rse.main.database.filesystem")


class FileSystemDatabase(Database):
    """A FileSystemDatabase writes raw json to files to a database."""

    database = "filesystem"

    def __init__(self, config_dir, config=None, **kwargs):
        """init for the filesystem ensures that the base folder (named
        according to the studyid) exists.
        """
        self.config = config
        self.create_database(config_dir)

    def create_database(self, config_dir):
        """Create the database. The parent folder must exist."""
        self.data_base = os.path.abspath(os.path.join(config_dir, "database"))
        if not os.path.exists(config_dir):
            raise DirectoryNotFoundError(
                config_dir, "must exist to create database there"
            )
        if not os.path.exists(self.data_base):
            mkdir_p(self.data_base)

    # Global

    def clear(self):
        """clear (delete) all software repositories."""
        for parser_dir in self.iter_parsers(fullpath=True):
            if os.path.exists(parser_dir):
                bot.info(f"Removing {parser_dir}")
                shutil.rmtree(parser_dir)
        return True

    # Get, delete, etc. only require uid

    def exists(self, uid):
        """Determine if a repo exists."""
        try:
            self.get(uid, exact=True)
            return True
        except:
            return False

    def add(self, uid, data=None):
        """Add a new software repository to the database."""
        if uid:
            parser = get_parser(uid, config=self.config)

            if not data:
                data = parser.get_metadata()
            else:
                parser.data = data

            # If it's a parser handoff
            if isinstance(data, ParserBase):
                parser = data
                data = parser.data

            if data:
                bot.info(f"{parser.uid} was added to the the database.")
                return SoftwareRepository(parser, data_base=self.data_base)
        else:
            bot.error("Please define a unique identifier to add.")

    def get_or_create(self, uid):
        """Determine if a repo exists."""
        try:
            repo = self.get(uid, exact=True)
        except:
            repo = self.add(uid)
        return repo

    def get(self, uid=None, exact=False):
        """Get a software repo based on a uid. If exact is not needed, we can
        search for a match based on the partial uid.  If exact is False,
        and a uid is not provided, get the last repository created.
        """
        if not uid and not exact:
            repos = get_latest_modified(self.data_base, pattern="metadata*.json")
            if repos:
                uid = (
                    repos.replace("metadata.json", "")
                    .replace(self.data_base, "")
                    .strip("/")
                )
            if not uid or not repos:
                raise NoReposError

        parser = get_parser(uid, config=self.config)
        return SoftwareRepository(parser, exists=True, data_base=self.data_base)

    def update(self, repo, rewrite=False, data=None):
        """
        Update a repository by retrieving metadata, and then calling update
        on the software repository to save it. If data is provided, we assume
        that a custom import is providing it.
        """
        data = data or repo.parser.get_metadata()
        if data:
            if rewrite:
                self.add(repo.uid)
            else:
                repo.update(updates=data)

    def label(self, repo, key, value, force=False):
        """
        Update a repository with a specific key/value pair.
        """
        if key in repo.data and not force:
            raise RuntimeError(
                f"{key} is already defined for {repo.uid}. Use --force to overwrite."
            )
        bot.debug(f"Adding key {key}:{value}")
        repo.update({key: value})

    def search(self, query, taxonomy=None, criteria=None):
        """
        A filesystem search can only support returning results with filenames.
        For taxonomy and criteria items, we load them and search.
        We organize results based on the query, taxonomy, and criteria
        The results returned are separate (e.g., a single repo can appear
        in more than one list).
        """
        results = {}

        taxonomy_regex = "(%s)" "|".join(taxonomy or [])
        criteria_regex = "(%s)" "|".join(criteria or [])
        for repo in self.list_repos():

            if query:
                if re.search(query, repo[0], re.IGNORECASE):
                    if query not in results:
                        results[query] = set()
                    results[query].add(repo[0])

            if taxonomy or criteria:
                repo = self.get(repo[0])

            # Add taxonomy items
            if taxonomy:
                for _, tags in repo.load_taxonomy().items():
                    for tag in tags:
                        if re.search(taxonomy_regex, tag, re.IGNORECASE):
                            if tag not in results:
                                results[tag] = set()
                            results[tag].add(repo.uid)

            # Add criteria items
            if criteria:
                for term, annotations in repo.load_criteria().items():
                    for _, annotation in annotations.items():
                        if annotation == "yes" and re.search(
                            criteria_regex, term, re.IGNORECASE
                        ):
                            if term not in results:
                                results[term] = set()
                            results[term].add(repo.uid)

        final = {}
        for key, listing in results.items():
            final[key] = [[x] for x in listing]
        return final

    def delete_repo(self, uid):
        """
        delete a repo based on a specific identifier.
        """
        if self.exists(uid):
            repo = self.get(uid)
            os.remove(repo.filename)

            # Remove the directory if no other repos
            dirname = os.path.dirname(repo.filename)
            if not os.listdir(dirname):
                shutil.rmtree(dirname)

            bot.info(f"{uid} has been removed.")
            return True

        bot.error(f"{uid} does not exist in the database.")
        return False

    def delete_parser(self, name):
        """
        delete all repos for a parser, based on executor's name (str).
        """
        parser_dir = os.path.join(self.data_base, name)
        if not os.path.exists(parser_dir):
            bot.info(f"Executor {parser_dir} directory does not exist.")
            return False
        shutil.rmtree(parser_dir)
        return True

    def iter_parsers(self, fullpath=False):
        """list executors based on the subfolders in the base database folder."""
        for contender in os.listdir(self.data_base):
            contender = os.path.join(self.data_base, contender)
            if os.path.isdir(contender):
                if not fullpath:
                    yield os.path.basename(contender)
                else:
                    yield contender

    def list_repos(self, name=None):
        """
        list software repositories, either under a particular parser name
        or just under all parsers. This returns repos in rows to be printed
        (or otherwise parsed).
        """
        listpath = self.data_base
        if name:
            listpath = os.path.join(listpath, name)
        rows = []
        for filename in recursive_find(listpath, pattern="metadata*.json"):
            rows.append(
                [
                    filename.replace("metadata.json", "")
                    .replace(self.data_base, "")
                    .strip("/")
                ]
            )
        return rows


class SoftwareRepository:
    """
    A software repository is a filesystem representation of a repo. It can
    take a uid, determine if the repo exists, and then interact with the
    metadata for it. If the repo is instantiated without a unique id
    it is assumed to not exist yet, otherwise it must already
    exist.
    """

    def __init__(self, parser, data_base, exists=False):
        """
        A SoftwareRepository holds some uid for a parser, and controls
        interaction with the filesystem.

        Arguments:
          parser (str)    : the parser
          data_base (str) : the path where the database exists.
          exists (bool)   : if True, must already exists (default is False)
        """
        self.uid = parser.uid
        self.parser = parser
        self.data_base = data_base
        self.data = {}
        self.criteria = {}
        self.taxonomy = {}
        self.create(exists)

    @property
    def url(self):
        return self.parser.get_url(self.data.get("data", ""))

    @property
    def avatar(self):
        return self.parser.get_avatar(self.data.get("data", ""))

    @property
    def description(self):
        return self.parser.get_description(self.data.get("data", ""))

    @property
    def filename(self):
        return os.path.join(self.parser_dir, "metadata.json")

    @property
    def parser_dir(self):
        return os.path.join(self.data_base, self.parser.uid)

    def update(self, updates=None):
        """
        Update a data file. This means reading, updating, and writing.
        """
        updates = updates or {}
        if "data" in (self.data or {}):
            self.data["data"] = update_nonempty(updates, self.data["data"])
        else:
            self.data = update_nonempty(updates, self.data or {})
        self.save()

    def update_criteria(self, uid, username, response):
        """
        Update a criteria, meaning adding a True/False answer to the
        unique id for the user. We are currently assuming that criteria
        have yes/no responses, and True == yes, False == no.
        """
        if uid not in self.criteria:
            self.criteria[uid] = {}
        if response:
            self.criteria[uid][username] = response

    def create(self, should_exist=False):
        """
        create the filename if it doesn't exist, otherwise if it should (and
        does not) exit on error.
        """
        if should_exist:
            if not os.path.exists(self.filename):

                # Might be provided prefix
                contenders = glob("%s*" % os.path.join(self.data_base, self.parser.uid))
                if len(contenders) == 1:
                    self.parser.uid = re.sub(
                        "(%s/|[.]json)" % self.data_base,
                        "",
                        contenders[0],
                    )

                elif len(contenders) > 1:
                    raise MultipleReposExistError(self.parser.uid)
                else:
                    raise RepoNotFoundError(self.parser.uid)
            self.data = self.load()
            self.taxonomy = self.load_taxonomy()
            self.criteria = self.load_criteria()

        if not os.path.exists(self.parser_dir):
            mkdir_p(self.parser_dir)

        # If it's the first time saving, create basic file
        if not should_exist:
            self.data = {
                "parser": self.parser.name,
                "uid": self.parser.uid,
                "url": self.parser.get_url(),
                "data": self.parser.export(),
            }
            self.save()

    def export(self):
        """
        wrapper to expose the executor.export function
        """
        return self.parser.export()

    def save(self):
        """
        Save a json object (metadata.json) for the software repository.
        """
        write_json(self.data, self.filename)

    def summary(self):
        return self.parser.summary()

    def load(self):
        """
        Given a software uid, load data from filename.
        """
        if os.path.exists(self.filename):
            return read_json(self.filename)

    def get_criteria(self):
        """
        Get loaded criteria
        """
        return self.criteria

    def get_taxonomy(self):
        """
        Get loaded taxonomy
        """
        return self.taxonomy

    def load_criteria(self):
        """
        Given a repository directory, load criteria files if they exist
        """
        criteria = {}
        for filename in glob(f"{self.parser_dir}/criteria*.tsv"):
            uid = (
                os.path.basename(filename).replace("criteria-", "").replace(".tsv", "")
            )
            content = read_file(filename)
            if uid not in criteria:
                criteria[uid] = {}
            for row in content:
                row = row.strip()
                if not row:
                    continue
                username, response = row.split("\t")
                criteria[uid][username] = response
        return criteria

    def save_criteria(self):
        """
        Save criteria to file. Each file is named based on the criteria id,
        and is a tab separated file that includes the username and response.
        """
        for uid, responses in self.criteria.items():
            filename = os.path.join(self.parser_dir, "criteria-%s.tsv" % uid)
            # Sort based on username
            rows = ["%s\t%s" % (k, v) for k, v in sorted(responses.items())]
            write_file("\n".join(rows), filename)
            bot.debug(f"{uid} saved to {filename}")

    def load_taxonomy(self):
        """
        Given a repository directory, load taxonomy annotations if they exist
        The taxonomy.tsv file should be a tab separated file with:
        username category-unique-id. This means that we keep a record of
        who has categorized what, and load this information into the
        taxonomy dictionary (organized by the category-unique-id which
        then has a total count and list of users).
        """
        taxonomy = {}
        taxonomy_file = os.path.join(self.parser_dir, "taxonomy.tsv")
        if os.path.exists(taxonomy_file):
            content = read_file(taxonomy_file)
            for row in content:
                row = row.strip()
                if not row:
                    continue
                username, uids = row.split("\t")
                taxonomy[username] = [x.strip() for x in uids.split(",")]
        return taxonomy

    def save_taxonomy(self):
        """
        Save taxonomy to file. Each file is named taxonomy.tsv,
        and is a tab separated file that includes the username and response.
        """
        filename = os.path.join(self.parser_dir, "taxonomy.tsv")
        rows = ["%s\t%s" % (k, ",".join(v)) for k, v in sorted(self.taxonomy.items())]
        write_file("\n".join(rows), filename)
        bot.debug(f"{self.uid} saved to {filename}")

    # Annotation

    def has_criteria_annotation(self, uid, username):
        """
        Determine if a repository has been annotated by a user.
        """
        if uid not in self.criteria:
            return False
        if username not in self.criteria[uid]:
            return False
        return True

    def has_taxonomy_annotation(self, username):
        """
        Determine if a repository has been annotated by a user.
        """
        if username not in self.taxonomy:
            return False
        return True
