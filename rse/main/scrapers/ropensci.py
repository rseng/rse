"""

Copyright (C) 2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.utils.urls import get_user_agent, check_response, repository_regex
from rse.main.parsers import get_parser, GitHubParser
import logging
import requests
import random
import re
from time import sleep

from .base import ScraperBase

bot = logging.getLogger("rse.main.scrapers.ropensci")


class ROpenSciScraper(ScraperBase):

    name = "ropensci"

    def __init__(self, query=None, **kwargs):
        super().__init__(query)

    def latest(self, paginate=False, delay=0.0):
        """
        Only return latest (top page) of results (default is sort by created)
        """
        return self.scrape(paginate=paginate, delay=delay)

    def search(self, query=None, paginate=True, delay=0.0):
        """
        Return all paginated results with search (no query accepted for now)
        """
        return self.scrape(paginate=paginate, delay=delay)

    def scrape(self, paginate=False, delay=None):
        """A shared function to scrape a set of repositories. Since the JoSS
        pages for a search and the base are the same, we can use a shared
        function.
        """
        parser = GitHubParser()
        repos = parser.get_org_repos("ropensci", paginate=paginate, delay=delay)

        for entry in repos:

            if not entry:
                continue

            # We determine software release based on the homepage url
            homepage = entry.get("homepage", "")
            if not homepage or "https://docs.ropensci.org" not in homepage:
                bot.info("Skipping repository: %s" % entry["html_url"])
                continue
            bot.info("Found repository: %s" % entry["html_url"])
            self.results.append(parser.parse_github_repo(entry))
        return self.results

    def create(self, database=None, config_file=None):
        """After a scrape (whether we obtain latest or a search query) we
        run create to create software repositories based on results.
        """
        from rse.main import Encyclopedia

        client = Encyclopedia(config_file=config_file, database=database)
        for result in self.results:
            uid = result["html_url"].split("//")[-1]

            # Add results that don't exist
            if not client.exists(uid):
                client.add(uid, data=result)
