"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import logging
import requests
from rse.utils.urls import check_response

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
        data = check_response(response)

        # Only save minimal set
        self.data = {}
        for key in [
            "name",
            "url",
            "full_name",
            "html_url",
            "private",
            "description",
            "created_at",
            "updated_at",
            "clone_url",
            "homepage",
            "size",
            "stargazers_count",
            "watchers_count",
            "language",
            "open_issues_count",
            "license",
            "subscribers_count",
        ]:
            if key in data:
                self.data[key] = data[key]
        self.data["owner"] = {}
        for key in ["html_url", "avatar_url", "login", "type"]:
            self.data["owner"][key] = data["owner"][key]

        return self.data
