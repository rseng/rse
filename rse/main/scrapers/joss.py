"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.utils.urls import get_user_agent
from rse.main.parsers import get_parser
import logging
import requests
import random
import sys
import re
from time import sleep

from .base import ScraperBase

bot = logging.getLogger("rse.main.scrapers.joss")


class JossScraper(ScraperBase):

    name = "joss"

    def __init__(self, query=None, **kwargs):
        super().__init__(query)

    def latest(self, paginate=False, delay=0.0):
        """The scraper should expose a function to populate self.results with
           some number of latest entries. Unlike a search, a latest scraper does
           not by default paginate. The user needs to interact directly with
           the Python client to do a scrape for all papers in JoSS.
        """
        url = "https://joss.theoj.org/papers/published.atom"
        return self.scrape(url, paginate=paginate, delay=delay)

    def search(self, query, paginate=True, delay=0.0):
        """The scraper should expose a function to populate self.results with
           a listing based on matching a search criteria.
        """
        url = "https://joss.theoj.org/papers/search?q=%s" % query
        return self.scrape(url, paginate=paginate, delay=delay)

    def scrape(self, url, paginate=False, delay=None):
        """A shared function to scrape a set of repositories. Since the JoSS
           pages for a search and the base are the same, we can use a shared
           function.
        """
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            sys.exit("BeautifulSoup is required. pip install rse[scraper].")

        # Handle pagination
        while url is not None:

            response = requests.get(url, headers={"User-Agent": get_user_agent()})
            soup = BeautifulSoup(response.text, "html.parser")
            url = None
            for link in soup.find_all("link", href=True):

                # Sleep for a random amount of time to give a rest!
                sleep(delay or random.choice(range(1, 10)) * 0.1)
                paper_url = link.attrs.get("href", "")

                # If we don't have the next page yet
                if link.attrs.get("rel") is not None and url is None and paginate:
                    if link.attrs.get("rel")[0] == "next":
                        url = link.attrs.get("href")

                # Retrieve page with paper metadata that we need
                if re.search(
                    "https://joss.theoj.org/papers/10.[0-9]{5}/joss.[0-9]{5}", paper_url
                ):
                    response = requests.get(
                        paper_url, headers={"User-Agent": get_user_agent()}
                    )
                    paper_soup = BeautifulSoup(response.text, "html5lib")

                    # Find links that we need
                    repo = {}
                    for link in paper_soup.find_all("a", href=True):
                        if "Software repository" in link.text:
                            repo["url"] = link.attrs.get("href", "")
                        elif "Software archive" in link.text:
                            repo["doi"] = link.attrs.get("href", "")

                    if repo.get("url") and repo.get("doi"):
                        bot.info("Found repository: %s" % repo["url"])
                        self.results.append(repo)

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
                client.label(repo.uid, key="doi", value=result.get("doi"))
