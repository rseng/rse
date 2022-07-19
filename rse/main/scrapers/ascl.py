"""

Copyright (C) 2022 Vanessa Sochat.

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

bot = logging.getLogger("rse.main.scrapers.ascl")


class AsclScraper(ScraperBase):

    name = "ascl"
    matchstring = "ascl"

    def __init__(self, query=None, **kwargs):
        super().__init__(query)
        self.baseurl = "https://ascl.net"

    def latest(self, paginate=False, delay=0.0):
        return self.scrape(paginate=paginate, delay=delay)

    def search(self, query, paginate=True, delay=0.0):
        return self.scrape(paginate=paginate, delay=delay, query=query)

    def scrape(self, paginate=False, delay=None, query=""):
        """
        A shared function to scrape software from molssi.
        """
        # Sort so newest first (latest)
        url = "%s/code/all/limit/250/dir/desc/order/date" % self.baseurl

        while url:
            response = requests.get(url, headers={"User-Agent": get_user_agent()})
            if response.status_code != 200:
                sys.exit("Unable to retrieve ASCL listing")
            next = self._parse_page(response)
            # Sleep for a random amount of time to give a rest!
            sleep(delay or random.choice(range(1, 10)) * 0.1)
            if paginate and next:
                url = next
            else:
                url = None

        return self.results

    def _parse_page(self, response):
        """
        Parse records from a single page
        """
        try:
            from bs4 import BeautifulSoup
            import bs4
        except ImportError:
            sys.exit("BeautifulSoup is required. pip install rse[scraper].")

        soup = BeautifulSoup(response.text, "html.parser")
        contenders = soup.find_all("div", {"class": "item"})
        for contender in contenders:

            # Get metadata from child
            for child in contender.children:
                if not isinstance(child, bs4.element.Tag):
                    continue
                result = {"doi": []}
                if "ascl_id" in child.attrs.get("class", []) and child.contents:
                    result["ascl_id"] = re.sub("(\n|\t)", "", child.text)

                    # Don't add submitted yet
                    if "submitted" in result["ascl_id"]:
                        continue

                elif "credit" in child.attrs.get("class", []) and child.contents:
                    result[
                        "credit"
                    ] = (
                        child.text
                    )  # [x.contents[0] for x in child.find_all('a') if x.contents]

                elif "abstract" in child.attrs.get("class", []) and child.contents:
                    result["description"] = child.text

                elif "title" in child.attrs.get("class", []) and child.contents:

                    # This has a link to the detail page
                    title = child.find_next("a")
                    if "href" not in title.attrs or not title.contents:
                        continue
                    result["title"] = title.contents[0]

                    # Go to the detail page
                    detail_url = "%s/%s" % (self.baseurl, title.attrs["href"])
                    response = requests.get(
                        detail_url, headers={"User-Agent": get_user_agent()}
                    )
                    if response.status_code != 200:
                        continue
                    details = BeautifulSoup(response.text, "html.parser")
                    links = details.find_all("dd")
                    for link in links:
                        ahref = link.find_next("a")
                        ref = ahref.attrs.get("href", "")
                        if "git" in ref:
                            result["url"] = ref
                        elif ref:
                            result["doi"].append(ref)
                    if "url" not in result:
                        continue
                    bot.info(f"Found record {result['url']}")
                    self.results.append(result)

        return self.find_next(soup)

    def find_next(self, soup):
        """
        Search through links and find next url
        """
        # For some reason this needs a double go?
        for i in range(2):
            for link in soup.find_all("a", href=True):
                if "Next" in link.text:
                    return self.baseurl + link.attrs["href"]

    def create(self, database=None, config_file=None, **kwargs):
        """
        After a scrape (whether we obtain latest or a search query) we
        run create to create software repositories based on results.
        """
        from rse.main import Encyclopedia

        client = Encyclopedia(config_file=config_file, database=database)
        for result in self.results:
            uid = result["url"].split("//")[-1]

            # If a repository is added that isn't represented
            try:
                uid = self.clean_uid(uid)
                repo = get_parser(uid)
            except Exception as exc:
                bot.warning(exc)
                continue

            # Add results that don't exist
            try:
                if not client.exists(repo.uid):
                    res = client.add(repo.uid)
                    res.update(result)

            # Some software is 404
            except:
                bot.error(f"Issue parsing {result}")
