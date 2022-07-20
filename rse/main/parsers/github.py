"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import logging
import random
import requests
from time import sleep
from rse.utils.urls import get_user_agent, check_response

from .base import ParserBase

bot = logging.getLogger("rse.main.parsers.github")


class GitHubParser(ParserBase):

    name = "github"
    matchstring = "github"

    def _set_uid(self, uid):
        """
        Given some kind of GitHub url, parse the uid
        """
        uid = uid.replace(":", "/")
        owner, repo = uid.replace(".git", "").split("/")[-2:]
        return "{}/{}".format(owner, repo)

    def load_secrets(self):
        """
        load secrets, namely the GitHub token
        """
        self.token = self.get_setting("TOKEN")

    def get_url(self, data=None):
        """
        a common function for a parser to return the html url for the
        upper level of metadata
        """
        data = data or self.data
        return data.get("html_url")

    def get_avatar(self, data=None):
        """
        a common function for a parser to return an image.
        """
        data = data or self.data
        return data.get("owner", {}).get("avatar_url", "")

    def get_description(self, data=None):
        """
        a common function for a parser to return a description.
        """
        data = data or self.data
        return data.get("description")

    def get_org_repos(self, org, paginate=True, delay=None):
        """
        A helper function to get a listing of org repos.
        """
        self.load_secrets()
        url = "https://api.github.com/orgs/%s/repos?per_page=100" % (org)
        headers = {
            "Accept": "application/vnd.github.symmetra-preview+json",
            "User-Agent": get_user_agent(),
        }
        if self.token:
            headers["Authorization"] = "token %s" % self.token

        repos = []

        # Start at 2, as 1 is implied to be the first
        page = 2
        original_url = url
        while url is not None:
            response = requests.get(url, headers=headers)
            data = check_response(response)

            # Reset the url to be None
            url = None
            if data and paginate:
                url = original_url + "&page=%s" % page

            repos = repos + data
            page += 1
            # Sleep for a random amount of time to give a rest!
            sleep(delay or random.choice(range(1, 10)) * 0.1)
        return repos

    def get_metadata(self, uri=None):
        """
        Retrieve repository metadata. The common metadata (timestamp) is
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
        if data is None:
            return None

        self.data = self.parse_github_repo(data)
        return self.data

    def parse_github_repo(self, repo):
        """
        Given an API response for a GitHub repository, parse a minimal set.
        """
        self.load_secrets()
        headers = {
            "Accept": "application/vnd.github.symmetra-preview+json",
        }
        if self.token:
            headers["Authorization"] = "token %s" % self.token

        # Only save minimal set
        data = {}
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
            if key in repo:
                data[key] = repo[key]
        data["owner"] = {}
        for key in ["html_url", "avatar_url", "login", "type"]:
            data["owner"][key] = repo["owner"][key]

        # Also try to get topics
        headers.update({"Accept": "application/vnd.github.mercy-preview+json"})
        url = "%s/topics" % repo["url"]
        response = requests.get(url, headers=headers)

        # Add topics on successful query
        topics = check_response(response)
        if topics is not None:
            data["topics"] = topics.get("names", [])

        # Add topics from another source
        if "topics" not in data and "topics" in repo:
            data["topics"] = repo["topics"]
        elif "topics" in data and "topics" in repo:
            data["topics"] += [x for x in repo["topics"] if x not in data["topics"]]

        return data
