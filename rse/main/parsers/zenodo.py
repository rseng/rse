"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import logging
import requests
import re

from .base import ParserBase

bot = logging.getLogger("rse.main.parsers.zenodo")


class ZenodoParser(ParserBase):

    name = "zenodo"
    matchstring = "^10[.][0-9]{4}/zenodo[.][0-9]{7}$"

    def __init__(self, uid=None, **kwargs):
        super().__init__(uid)

    def _set_uid(self, uid):
        """Given some kind of Zenodo uri, parse it
        """
        match = re.search(self.matchstring, uid)
        if not match:
            raise RuntimeError(f"{uid} does match a Zenodo DOI.")
        return match.group()

    def load_secrets(self):
        """load secrets, namely the access token, check if required and
           exit if not provided
        """
        self.token = self.get_setting("TOKEN")

    def get_url(self, data=None):
        """a common function for a parser to return the html url for the
           upper level of metadata
        """
        data = data or self.data
        return data.get("links", {}).get("html")

    def get_avatar(self, data=None):
        """a common function for a parser to return an image.
        """
        data = data or self.data
        return data.get("links", {}).get("badge")

    def get_description(self, data=None):
        """a common function for a parser to return a description.
        """
        data = data or self.data
        return data.get("metadata", {}).get("description")

    def get_metadata(self, uri=None, require_repo=True):
        """Retrieve repository metadata. The common metadata (timestamp) is
           added by the software repository parser, and here we need to
           ensure that the url field is populated with a correct url.

           Arguments:
           uri (str) : a repository uri string to override one currently set
           require_repo (bool) : require a repository to parse.
        """
        from rse.main.parsers import get_parser
        from rse.utils.urls import repository_regex

        repository_regex = repository_regex.rstrip("$")

        if uri:
            self.set_uri(uri)
        self.load_secrets()

        # Get the record number from the doi
        record = self.uid.split("/")[-1].replace("zenodo.", "")

        # Token isn't required for public entries
        if self.token:
            response = requests.get(
                "https://zenodo.org/api/records/%s" % record,
                json={"access_token": self.token},
            )
        else:
            response = requests.get("https://zenodo.org/api/records/%s" % record)

        # Successful query!
        if response.status_code == 200:
            self.data = response.json()

            # For Zenodo, we require a GitHub or GitLab related identifier to add
            repo_url = None
            for identifier in self.data["metadata"].get("related_identifiers", []):
                match = re.search(repository_regex, identifier["identifier"])
                if match:
                    repo_url = "https://%s" % match.group()
                    break

            # If we return None, the entry is not added
            if repo_url is None and require_repo is True:
                bot.warning(
                    "Repository url not found with Zenodo record, skipping add."
                )
                return repo_url

            # Convert the class into another parser type
            elif repo_url is not None:
                uid = self.uid
                self = get_parser(repo_url)
                self.get_metadata()
                self.data["doi"] = uid
                return self
            return self.data

        elif response.status_code == 404:
            bot.error(f"Cannot find doi {self.uid}.")

        elif response.status_code in [400, 401, 403]:
            bot.error(f"Permission denied to query {self.uid}")

        else:
            bot.error(
                f"Cannot get doi {self.uid}: {response.status_code}, {response.reason}"
            )
        return None
