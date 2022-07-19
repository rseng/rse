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
from time import sleep

from .base import ScraperBase

bot = logging.getLogger("rse.main.scrapers.molssi")


class MolssiScraper(ScraperBase):

    name = "molssi"
    matchstring = "molssi"

    def __init__(self, query=None, **kwargs):
        super().__init__(query)
        self.baseurl = "https://api.molssi.org"

    def latest(self, paginate=False, delay=0.0):
        return self.scrape(paginate=paginate, delay=delay)

    def search(self, query, paginate=True, delay=0.0):
        return self.scrape(paginate=paginate, delay=delay, query=query)

    def scrape(self, paginate=False, delay=None, query=""):
        """
        A shared function to scrape software from molssi.
        """
        url = "%s/search" % self.baseurl
        try:
            from bs4 import BeautifulSoup
            import bs4
        except ImportError:
            sys.exit("BeautifulSoup is required. pip install rse[scraper].")

        data = {
            "domain": "",
            "languages": "[]",
            "mm_filters": None,
            "price": "",
            "qm_filters": "{}",
            "query_text": query,
        }

        response = requests.get(
            url, params=data, headers={"User-Agent": get_user_agent()}
        )
        soup = BeautifulSoup(response.text, "html.parser")
        contenders = soup.find_all("a", {"class": "card-link"}, href=True)
        for contender in contenders:
            href = contender.attrs.get("href")
            if "software_detail" not in href:
                continue

            href = "%s/%s" % (self.baseurl, href)

            # Sleep for a random amount of time to give a rest!
            sleep(delay or random.choice(range(1, 10)) * 0.1)
            response = requests.get(href, headers={"User-Agent": get_user_agent()})
            meta_soup = BeautifulSoup(response.text, "html5lib")
            links = meta_soup.find_all("a", href=True)

            source_code = None
            citation = None
            for link in links:
                if "source code" in link.text.lower():
                    source_code = link.attrs.get("href")

                    if (
                        source_code
                        and "github" in source_code
                        or "gitlab" in source_code
                    ):
                        break
                    if (
                        source_code
                        and "github" not in source_code
                        or "gitlab" not in source_code
                    ):
                        source_code = None

            # If no source code, continue parsing until we find
            if not source_code:
                for link in links:
                    href = link.attrs.get("href")
                    if href and "github" in href or "gitlab" in href:
                        source_code = href
                        break

            # We couldn't find the source code
            if not source_code:
                continue

            # Do we have a citation?
            for bolded in meta_soup.find_all("b"):
                if "citation" in bolded.text.lower():
                    if "row" in bolded.parent.parent.attrs.get("class"):
                        nexts = list(bolded.parent.parent.parent.next_elements)
                        for next_element in nexts:

                            # The citation is the first link under this bolded section
                            if isinstance(
                                next_element, bs4.element.Tag
                            ) and next_element.find_next("a"):
                                citation = next_element.find_next("a")
                                citation = citation.attrs.get("href")
                                break

            # These are not citations!
            if citation and ("mailto" in citation or citation == source_code):
                citation = None

            repo = None
            if source_code and citation:
                bot.info("Found repository %s and doi %s" % (source_code, citation))
                repo = {"url": source_code, "doi": citation}
            elif source_code:
                bot.info("Found repository %s" % source_code)
                repo = {"url": source_code}

            if repo:
                self.results.append(repo)

        return self.results

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
                repo = get_parser(uid)
            except NotImplementedError as exc:
                bot.warning(exc)
                continue

            # Add results that don't exist
            if not client.exists(repo.uid):
                client.add(repo.uid)
                client.label(repo.uid, key="doi", value=result.get("doi"))
