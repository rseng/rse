"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main.config import Config
from rse.defaults import RSE_DATABASE, RSE_PARSERS, RSE_CONFIG_FILE

from rse.exceptions import RepoNotFoundError, RepoMetadataExistError
from rse.main.database import init_db
from rse.utils.prompt import confirm, choice_prompt
from rse.utils.file import read_file
from rse.utils.command import get_github_username
from rse.utils.urls import repository_regex
from rse.main.parsers import get_parser
from rse.main.criteria import get_criteria
from rse.main.taxonomy import get_taxonomy
from rse.logger.message import bot as message

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

    def label(self, uid, key, value, force=False):
        """Update an existing software repository with a specific label.
        """
        try:
            repo = self.get(uid)
            self.db.label(repo, key, value, force=force)
            bot.info(f"{repo.uid} has been updated.")
            return repo
        except RepoMetadataExistError:
            bot.error(
                f"{repo.uid} already has value for {key}. Use --force to overwrite."
            )
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

    # Save Handlers

    def save_criteria(self, repo):
        """Given a repository that can be a handle to a filesystem entry
           or database, save the criteria
        """
        # The filesystem database saves at the end
        if hasattr(repo, "save_criteria"):
            repo.save_criteria()

        # Relational saves the database item
        else:
            self.db.update(repo)

    def save_taxonomy(self, repo, username, uids):
        """Given a repository that can be a handle to a filesystem entry
           or database, save the criteria
        """
        if hasattr(repo, "save_taxonomy"):
            repo.taxonomy[username] = uids
            repo.save_taxonomy()
        else:
            repo.update_taxonomy(username, uids)
            self.db.update(repo)

    # Metrics
    def analyze_bulk(
        self,
        cthresh=0.5,
        tthresh=1,
        taxonomy_uids=None,
        criteria_uids=None,
        include_empty=False,
    ):
        """analyze takes a repository and calculates a "final answer" based on user provided
           thresholds
        """
        results = []
        for repo in self.list():
            result = self.analyze(
                repo[0],
                cthresh=cthresh,
                tthresh=tthresh,
                taxonomy_uids=taxonomy_uids,
                criteria_uids=criteria_uids,
            )
            if not result["taxonomy"] and not result["criteria"] and not include_empty:
                continue
            results.append(result)
        return results

    def analyze(
        self, repo, cthresh=0.5, tthresh=1, taxonomy_uids=None, criteria_uids=None
    ):
        """analyze takes a repository and calculates a "final answer" based on user provided
           thresholds
        """
        # If taxonomy or criteria lists aren't defined, use all
        if not taxonomy_uids:
            taxonomy_uids = [x["uid"] for x in self.list_taxonomy()]
        if not criteria_uids:
            criteria_uids = [x["uid"] for x in self.list_criteria()]

        parser = get_parser(repo, config=self.config)
        repo = self.get(parser.uid)
        metrics = {"repo": parser.uid, "criteria": {}, "taxonomy": {}}

        # Calculate "final" answers for each criteria based on votes and threshold
        counts = {}
        for name, votes in repo.get_criteria().items():
            # Skip criteria if not important
            if name not in criteria_uids:
                continue
            if name not in counts:
                counts[name] = {"yes": 0, "no": 0, "total": 0}
            for username, response in votes.items():
                counts[name][response] += 1
                counts[name]["total"] += 1

        # Calculate final answers!
        for name, summary in counts.items():
            if summary["yes"] / summary["total"] >= cthresh:
                metrics["criteria"][name] = "yes"
            else:
                metrics["criteria"][name] = "no"

        counts = {}
        for username, categories in repo.get_taxonomy().items():
            for category in categories:
                if category not in counts:
                    counts[category] = 0
                counts[category] += 1

        # Include those above the requested threshold
        for name, count in counts.items():
            if count >= tthresh:
                metrics["taxonomy"][name] = count

        return metrics

    def summary(self, repo=None):
        """Summarize metrics for the entire database if uid is not defined,
           or one specific repository.
        """
        if repo is None:
            repos = self.list()
            metrics = {"repos": len(repos)}
        else:
            parser = get_parser(repo, config=self.config)
            repos = [[parser.uid]]
            metrics = {"repo": parser.uid}

        # Add taxonomy and criteria items
        metrics["taxonomy-count"] = len(self.list_taxonomy())
        metrics["criteria-count"] = len(self.list_criteria())
        metrics["users"] = {}
        metrics["taxonomy"] = {}
        metrics["criteria"] = {}

        # Count annotations for
        for repo in repos:
            parser = get_parser(repo[0], config=self.config)
            repo = self.get(parser.uid)

            if not repo.criteria and not repo.taxonomy:
                continue

            # Add repository to summary metrics
            metrics["taxonomy"][repo.uid] = {}
            metrics["criteria"][repo.uid] = {}

            # Derive all users that have annotated taxonomy/criteria
            users = set()
            for name, votes in repo.get_criteria().items():
                [users.add(user) for user in votes.keys()]
                if name not in metrics["criteria"][repo.uid]:
                    metrics["criteria"][repo.uid] = {"yes": 0, "no": 0}
                for vote in votes.values():
                    metrics["criteria"][repo.uid][vote] += 1

            # Update criteria annotations
            for user in users:
                if user not in metrics["users"]:
                    metrics["users"][user] = {
                        "criteria-annotations": 0,
                        "taxonomy-annotations": 0,
                    }
                metrics["users"][user]["criteria-annotations"] += 1

            # Derive all users that have annotated taxonomy/criteria
            users = set()
            for username, categories in repo.get_taxonomy().items():
                users.add(username)
                for category in categories:
                    if category not in metrics["taxonomy"][repo.uid]:
                        metrics["taxonomy"][repo.uid][category] = 0
                    metrics["taxonomy"][repo.uid][category] += 1

            # Don't add empty entries
            if not repo.taxonomy and repo.uid in metrics["taxonomy"]:
                del metrics["taxonomy"][repo.uid]

            if not repo.criteria and repo.uid in metrics["criteria"]:
                del metrics["criteria"][repo.uid]

        # Add unique users
        metrics["users-count"] = len(metrics["users"])
        return metrics

    # Annotation

    def annotate(self, username, atype, unseen_only=True, repo=None, save=False):
        """Annotate the encyclopedia, either for criteria or taxonomy.
           A username is required for the namespace.
 
           Arguments:
            - username (str) : the user's GitHub username
            - atype (str) : the annotation type
            - unseen_only (bool): annotate only items not seen by username
            - repo (str) : annotate a particular software repository
        """
        # git config user.name
        if not username:
            username = get_github_username()

        if atype == "criteria":
            return self.annotate_criteria(username, unseen_only, repo, save)
        elif atype == "taxonomy":
            return self.annotate_taxonomy(username, unseen_only, repo, save)
        bot.error(f"Unknown annotation type, {atype}.")

    def _import_annotation(self, input_file, username, stop_line="## Criteria"):
        """A general helper (private)  function to import an annotation, meaning
           we parse a repository and return additional lines for parsing.
        """
        if not username or not input_file:
            raise RuntimeError(
                "A username and input file are required to import annotation criteria."
            )

        if not os.path.exists(input_file):
            raise FileNotFoundError(input_file)

        lines = read_file(input_file)
        line = lines.pop(0)

        # Find the repository name
        while stop_line not in line:
            match = re.search(repository_regex, line)
            if match:
                break
            line = lines.pop(0)

        # Retrieve the match
        if not match:
            raise RuntimeError(f"repository pattern not found in {input_file}")
        reponame = match.group()
        parser = get_parser(reponame)
        repo = self.get(parser.uid)
        return repo, lines

    def import_criteria_annotation(self, input_file, username):
        """Given a text file that has a bullet list of (some checked) criteria
           as might be generated in a GitHub issue, read in the file and the
           username to do an annotation. If a user has already done an annotation,
           his or her record is updated.
        """
        repo, lines = self._import_annotation(input_file, username)

        # Now iterate through checklist, update
        for line in lines:
            uid = line.split("criteria-")[-1].strip()
            if "[x]" in line:
                repo.update_criteria(uid, username, "yes")
                print(f"Updating {repo.uid}: {uid}->yes")
            elif re.search("\[]|\[ \]", line):
                repo.update_criteria(uid, username, "no")
                print(f"Updating {repo.uid}: {uid}->no")

        # Save the criteria
        self.save_criteria(repo)

    def import_taxonomy_annotation(self, input_file, username):
        """Given a text file that has a bullet list of (some checked) criteria
           as might be generated in a GitHub issue, read in the file and the
           username to do an annotation. If a user has already done an annotation,
           his or her record is updated.
        """
        repo, lines = self._import_annotation(
            input_file, username, stop_line="## Taxonomy"
        )

        # Now iterate through checklist, update
        uids = []
        for line in lines:
            if "RSE-taxonomy" not in line or "[x]" not in line:
                continue
            uid = line.split("]")[-1].strip()
            if uid.startswith("RSE-taxonomy") and uid not in uids:
                print(f"{repo.uid} adding {uid}")
                uids.append(uid)
        self.save_taxonomy(repo, username, uids)

    def yield_criteria_annotation_repos(self, username, unseen_only=True, repo=None):
        """Given a username, repository, and preference for seen / unseen,
           yield a repository to annotate.
        """
        if repo is None:
            repos = self.list()
        else:
            parser = get_parser(repo, config=self.config)
            repos = [[parser.uid]]
            unseen_only = False

        # yield combinations that don't exist yet, repo first to save changes
        for name in repos:
            repo = self.get(name[0])
            for item in self.list_criteria():
                if unseen_only and not repo.has_criteria_annotation(
                    item["uid"], username
                ):
                    yield repo, item
                elif not unseen_only:
                    yield repo, item

    def yield_taxonomy_annotation_repos(self, username, unseen_only=True, repo=None):
        """Given a username, repository, and preference for seen / unseen,
           yield a repository to annotate.
        """
        if repo is None:
            repos = self.list()
        else:
            parser = get_parser(repo, config=self.config)
            repos = [[parser.uid]]
            unseen_only = False

        # yield combinations that don't exist yet, repo first to save changes
        for name in repos:
            repo = self.get(name[0])
            if unseen_only and not repo.has_taxonomy_annotation(username):
                yield repo
            elif not unseen_only:
                yield repo

    def annotate_criteria(self, username, unseen_only=True, repo=None, save=False):
        """Annotate criteria, meaning we iterate over repos and criteria that 
           match the user request, namely to annotate unseen only, or just
           a particular repository. If the repository is specified, unseen_only
           is assumed False.
        """
        annotations = {}
        last = None
        for repo, criteria in self.yield_criteria_annotation_repos(
            username, unseen_only, repo
        ):

            # Only print repository if not seen yet
            if not last or repo.uid != last.uid:

                # If we have a last repo, we need to save progress
                if last is not None and save is True:
                    self.save_criteria(last)

                if last is not None:
                    annotations[last.uid] = last.criteria

                message.info(f"\n{repo.url} [{repo.description}]:")
                last = repo

            response = choice_prompt(
                criteria["name"],
                choices=["y", "Y", "n", "N", "s", "S", "skip"],
                choice_prefix="y/n or s to skip",
            )

            # The user can skip an answer if wanted
            if response in ["s", "S", "skip"]:
                continue

            repo.update_criteria(criteria["uid"], username, response)

        # Save the last repository
        if last is not None and save is True:
            self.save_criteria(last)

        if last is not None:
            annotations[last.uid] = last.criteria
        return annotations

    def annotate_taxonomy(self, username, unseen_only=True, repo=None, save=False):
        """Annotate taxonomy, meaning we iterate over repos and criteria that 
           match the user request, namely to annotate unseen only, or just
           a particular repository. If the repository is specified, unseen_only
           is assumed False.
        """
        annotations = {}

        # Retrieve the full taxonomy
        items = self.list_taxonomy()
        choices = [str(i) for i, _ in enumerate(items)] + ["s", "S", "skip"]
        prefix = "0:%s or s to skip" % (len(items) - 1)

        for repo in self.yield_taxonomy_annotation_repos(username, unseen_only, repo):

            message.info(f"\n{repo.url} [{repo.description}]:")
            print("How would you categorize this software? [enter one or more numbers]")
            for i, t in enumerate(items):
                example = t.get("example", "")
                name = t.get("name", "")
                if name and example:
                    print(f"[{i}] {name} ({example})")
                elif name:
                    print(f"[{i}] {name}")

            response = choice_prompt(
                "Please enter one or more numbers, separated by spaces",
                choices=choices,
                choice_prefix=prefix,
                multiple=True,
            )

            if response in ["s", "S", "skip"]:
                continue

            # Get the unique ids
            uids = [
                items[int(x)]["uid"]
                for x in set(response.split(" "))
                if int(x) < len(items)
            ]

            # Filesystem database we write filename to repository folder
            self.save_taxonomy(repo, username, uids)
            annotations[repo.uid] = repo.taxonomy

        return annotations
