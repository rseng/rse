"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.utils.urls import get_user_agent, check_response, repository_regex
from rse.main.parsers import get_parser
import logging
import requests
import re
import time

from .base import ScraperBase

bot = logging.getLogger("rse.main.scrapers.hal")

# Allow the regex to have newline at end
repository_regex = repository_regex.strip("$")


class HalScraper(ScraperBase):

    name = "hal"
    matchstring = "hal"

    def __init__(self, query=None, **kwargs):
        super().__init__(query)

    def latest(self, paginate=False, delay=0.0):
        """
        populate self.results with some number of latest entries. Unlike
        a search, a latest scraper does not by default paginate. Hal will by
        default return all entries, so the user is required to define a number
        for latest.
        """
        url = "https://api.archives-ouvertes.fr/search/?q=github&fq=docType_s:(SOFTWARE)&wt=json"
        return self.scrape(url, delay=delay)

    def search(self, query, paginate=True, delay=0.0):
        """
        populate self.results with a listing based on matching a search criteria.
        We search the description.
        """
        url = (
            "http://api.archives-ouvertes.fr/search/?q=%s&fq=docType_s:(SOFTWARE)&wt=json"
            % query
        )
        return self.scrape(url, delay=delay)

    def scrape(self, url, paginate=False, delay=0.0):
        """
        A shared function to scrape a set of repositories.
        """
        # Api doesn't appear to have pagination
        response = requests.get(url, headers={"User-Agent": get_user_agent()})
        data = check_response(response)

        for entry in data.get("response", {}).get("docs", []):
            page_url = entry["uri_s"]
            response = requests.get(page_url, headers={"User-Agent": get_user_agent()})
            repo_url = None
            if response.status_code == 200:
                match = re.search(repository_regex, response.text, re.IGNORECASE)
                if match:
                    repo_url = match.group()

            if repo_url:
                bot.info("Found repository: %s" % repo_url)
                self.results.append(repo_url)
            time.sleep(delay)

        return self.results

    def create(self, database=None, config_file=None, **kwargs):
        """
        After a scrape (whether we obtain latest or a search query) we
        run create to create software repositories based on results.
        """
        from rse.main import Encyclopedia

        client = Encyclopedia(config_file=config_file, database=database)
        for repo_id in self.results:
            repo = get_parser(repo_id)

            # Add results that don't exist
            if not client.exists(repo.uid):
                client.add(repo.uid)
