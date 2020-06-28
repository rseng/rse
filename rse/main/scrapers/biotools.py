"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.utils.urls import get_user_agent, check_response, repository_regex
from rse.main.parsers import get_parser
import logging
import requests
import random
import re
from time import sleep

from .base import ScraperBase

bot = logging.getLogger("rse.main.scrapers.biotools")


class BioToolsScraper(ScraperBase):

    name = "biotools"

    def __init__(self, query=None, **kwargs):
        super().__init__(query)

    def latest(self, paginate=False, delay=0.0):
        """populate self.results with some number of latest entries. Unlike 
           a search, a latest scraper does not by default paginate. The user 
           needs to interact directly with the Python client to scrape all.
        """
        url = "https://bio.tools/api/tool/?format=json"
        return self.scrape(url, paginate=paginate, delay=delay)

    def search(self, query, paginate=True, delay=0.0):
        """populate self.results with a listing based on matching a search criteria.
           we search the description.
        """
        url = 'https://bio.tools/api/t/?description="%s"&format=json' % query
        return self.scrape(url, paginate=paginate, delay=delay)

    def scrape(self, url, paginate=False, delay=None):
        """A shared function to scrape a set of repositories. Since the JoSS
           pages for a search and the base are the same, we can use a shared
           function.
        """
        # Handle pagination
        original_url = url
        while url is not None:

            response = requests.get(url, headers={"User-Agent": get_user_agent()})
            data = check_response(response)

            # Reset the url to be None
            url = None
            if data.get("next") and paginate:
                url = original_url + "&page=%s" % data.get("next", "").replace(
                    "?page=", ""
                )

            for entry in data.get("list", []):

                # Look for GitHub / GitLab URL
                repo = {}
                for link in entry.get("link", []):
                    if "Repository" in link["type"] and re.search(
                        repository_regex, link["url"], re.IGNORECASE
                    ):
                        repo["url"] = link["url"]

                # If we don't have a repository, search the homepage
                if not repo.get("url") and re.search(
                    repository_regex, entry["homepage"]
                ):
                    repo["url"] = entry["homepage"]

                # We must have a repository url to parse
                if not repo.get("url"):
                    continue

                # Look for a doi
                for pub in entry["publication"]:
                    if pub.get("doi"):
                        repo["doi"] = pub.get("doi")

                bot.info("Found repository: %s" % repo["url"])
                self.results.append(repo)

                # Sleep for a random amount of time to give a rest!
                sleep(delay or random.choice(range(1, 10)) * 0.1)

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
                if result.get("doi") is not None:
                    client.label(repo.uid, key="doi", value=result.get("doi"))
