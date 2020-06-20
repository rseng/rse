"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import logging
import requests

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
        """load secrets, namely the GitHub token
        """
        self.token = self.get_setting("TOKEN")

    def get_url(self, data=None):
        """a common function for a parser to return the html url for the
           upper level of metadata
        """
        data = data or self.data
        return data.get("html_url")

    def get_avatar(self, data=None):
        """a common function for a parser to return an image.
        """
        data = data or self.data
        return data.get("owner", {}).get("avatar_url", "")

    def get_description(self, data=None):
        """a common function for a parser to return a description.
        """
        data = data or self.data
        return data.get("description")

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
            "Accept": "application/vnd.github.symmetra-preview+json",
        }
        if self.token:
            headers["Authorization"] = "token %s" % self.token

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
                f"Cannot get repo {repo}: {response.status_code}, {response.reason}"
            )
        return None
