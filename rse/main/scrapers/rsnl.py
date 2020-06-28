"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.utils.urls import get_user_agent, check_response
from rse.main.parsers import get_parser
import logging
import requests
import time

from .base import ScraperBase

bot = logging.getLogger("rse.main.scrapers.rsnl")

# Research Software Netherlands
class RSNLScraper(ScraperBase):

    name = "rsnl"

    def __init__(self, query=None, **kwargs):
        super().__init__(query)

    def latest(self, paginate=False, delay=0.0):
        """The scraper should expose a function to populate self.results with
           some number of latest entries. Unlike a search, a latest scraper does
           not by default paginate.
        """
        url = "https://research-software.nl/api/software"
        return self.scrape(url, delay=delay)

    def search(self, query, paginate=True, delay=0.0):
        """The scraper should expose a function to populate self.results with
           a listing based on matching a search criteria.
        """
        # Haven't figured out a way to search
        bot.warning(
            "The RSNL scraper does not support search, returning latest instead."
        )
        return self.latest(paginate, delay=delay)

    def scrape(self, url, paginate=False, delay=0.0):
        """A shared function to scrape a set of repositories. Since the JoSS
           pages for a search and the base are the same, we can use a shared
           function.
        """
        response = requests.get(url, headers={"User-Agent": get_user_agent()})
        data = check_response(response) or []

        for entry in data:

            # I only see GitHub urls
            repo_url = entry.get("repositoryURLs", {}).get("github")
            repo_url = repo_url[0] if repo_url else None
            doi = entry.get("conceptDOI")
            doi = doi if doi and "FIXME" not in doi else None
            if repo_url and doi:
                bot.info("Found repository: %s" % repo_url)
                self.results.append({"url": repo_url, "doi": doi})
            elif repo_url:
                bot.info("Found repository: %s" % repo_url)
                self.results.append({"url": repo_url})
            time.sleep(delay)

        return self.results

    def create(self, database=None, config_file=None):
        """After a scrape (whether we obtain latest or a search query) we
           run create to create software repositories based on results.
        """
        from rse.main import Encyclopedia

        client = Encyclopedia(config_file=config_file, database=database)
        for result in self.results:
            uid = result["url"].split("//")[-1]
            repo = get_parser(uid)

            # Add results that don't exist
            if not client.exists(repo.uid):
                client.add(repo.uid)
                if result.get("doi"):
                    client.label(repo.uid, key="doi", value=result.get("doi"))
