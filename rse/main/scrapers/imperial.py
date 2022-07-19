"""

Copyright (C) 2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.utils.urls import get_user_agent, repository_regex
from rse.main.parsers import get_parser
import logging
import requests
import sys
import re
import csv

from .base import ScraperBase

bot = logging.getLogger("rse.main.scrapers.imperial")

# Allow the regex to have newline at end
repository_regex = repository_regex.strip("$")

csv_url = "https://raw.githubusercontent.com/ImperialCollegeLondon/research-software-directory/main/repos.csv"


class ImperialCollegeLondonScraper(ScraperBase):

    name = "imperial"
    matchstring = "imperial"

    def __init__(self, query=None, **kwargs):
        super().__init__(query)

    def latest(self, paginate=False, delay=0.0):
        """
        Populate self.results with some number of latest entries.
        """
        return self.scrape(csv_url, delay=delay)

    def search(self, query, paginate=True, delay=0.0):
        """
        Populate self.results with a listing based on matching a search criteria.
        """
        return self.scrape(csv_url, delay=delay)

    def scrape(self, url, paginate=False, delay=0.0):
        """
        A shared function to scrape a set of repositories.
        """
        # Api doesn't appear to have pagination
        response = requests.get(url, headers={"User-Agent": get_user_agent()})
        if response.status_code != 200:
            bot.error("Could not retrieve data from %s" % url)
            sys.exit()

        reader = csv.reader(response.text.split("\n"))
        parsed = [x for x in list(reader) if x]
        headers = parsed.pop(0)

        # Lookup based on index
        headers = {k: i for i, k in enumerate(headers)}
        for row in parsed:
            repo = row[headers["url"]]
            match = re.search(repository_regex, repo, re.IGNORECASE)
            repo_url = None
            if match:
                repo_url = match.group()

            if repo_url:
                meta = {k: row[i] for k, i in headers.items()}
                entry = {k: v for k, v in meta.items() if v}
                bot.info("Found repository: %s" % repo_url)
                self.results.append(entry)

        return self.results

    def create(self, database=None, config_file=None, **kwargs):
        """
        After a scrape (whether we obtain latest or a search query) we
        run create to create software repositories based on results.
        """
        from rse.main import Encyclopedia

        client = Encyclopedia(config_file=config_file, database=database)
        for entry in self.results:
            repo = get_parser(entry["url"])

            # Add results that don't exist
            if not client.exists(repo.uid):
                client.add(repo.uid)
                for k, v in entry.items():
                    if k == "url" or not v:
                        continue
                client.label(repo.uid, k, v, force=True)
