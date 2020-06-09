"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import logging
import requests
import sys

from .base import ParserBase

bot = logging.getLogger("rse.main.parsers.github")


class GitHubParser(ParserBase):

    name = "github"
    matchstring = "github"

    def __init__(self, uid=None, **kwargs):
        super().__init__(uid)

    def _set_uid(self, uid):
        """Given some kind of GitHub url, parse the uid
        """
        uid = uid.replace(":", "/")
        owner, repo = uid.replace(".git", "").split("/")[-2:]
        return "{}/{}".format(owner, repo)

    def load_secrets(self):
        """load secrets, namely the GitHub token, check if required and
           exit if not provided
        """
        self.token = self.get_setting("TOKEN")
        if not self.token:
            sys.exit("RSE_GITHUB_TOKEN is required")

    def get_url(self):
        """a common function for a parser to return the html url for the
           upper level of metadata
        """
        return self.data.get("html_url")

    def get_metadata(self, uri=None):
        """Retrieve repository metadata. The common metadata (timestamp) is
           added by the software repository parser, and here we need to
           ensure that the url field is populated with a correct url.

           Arguments:
           uri (str) : a repository uri string to override one currently set
        """
        if uri:
            self.set_uri(uri)
        self.load_secrets()
        repo = "/".join(self.uid.split("/")[-2:])
        url = "https://api.github.com/repos/%s" % (repo)
        headers = {
            "Authorization": "token %s" % self.token,
            "Accept": "application/vnd.github.symmetra-preview+json",
        }

        response = requests.get(url, headers=headers)

        # Successful query!
        if response.status_code == 200:
            self.data = response.json()
            return self.data

        elif response.status_code == 404:
            bot.error(f"Cannot find repository {repo}.")

        elif response.status_code in [400, 401, 403]:
            bot.error(f"Permission denied to query {repo}")

        else:
            bot.error(
                "Cannot get repo {repo}: {response.status_code}, {response.reason}"
            )
        return None
