"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""


class Database:
    """A rse database holds common functions to represent repos, and metadata.
    """

    database = "notimplemented"

    def clear(self):
        """clear (delete) all software repositories.
        """
        raise NotImplementedError

    def get(self):
        """get a software repository from the database.
        """
        raise NotImplementedError

    def exists(self):
        """determine if a software repository exists in the database.
        """
        raise NotImplementedError

    def search(self, query):
        """search is only available to non-filesystem databases
        """
        raise NotImplementedError

    def update(self, uid):
        """update a software repository.
        """
        raise NotImplementedError

    def add(self, uid):
        """Add a new software repository to the database.
        """
        raise NotImplementedError

    def get_or_create(self, uid):
        """Determine if a repo exists.
        """
        raise NotImplementedError

    def delete_repo(self, uid):
        """delete a repo based on a specific identifier.
        """
        raise NotImplementedError

    def delete_parser(self, name):
        """delete all repos for a parser based on the parser name.
        """
        raise NotImplementedError

    def list_repos(self, name=None):
        """list software repositories, either under a particular parser name
           or just under all parsers.
        """
        raise NotImplementedError
