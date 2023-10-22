"""

Copyright (C) 2022-2023 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import logging

from rse.main.parsers import get_parser
from rse.utils.strings import update_nonempty

from .base import ScraperBase

bot = logging.getLogger("rse.main.scrapers.biogrids")


class BioGridsScraper(ScraperBase):
    name = "biogrids"
    matchstring = "biogrids"

    def __init__(self, query=None, **kwargs):
        super().__init__(query)
        self.baseurl = "https://biogrids.org/software/"

    def latest(self, paginate=False, delay=0.0):
        return self.scrape(paginate=paginate, delay=delay)

    def search(self, query, paginate=True, delay=0.0):
        return self.scrape(paginate=paginate, delay=delay, query=query)

    def scrape(self, paginate=False, delay=None, query=""):
        """
        A shared function to scrape software from biogrids.
        """
        soup = self.soupify(self.baseurl)
        contenders = soup.find_all(
            "tr", {"itemtype": "http://schema.org/SoftwareApplication"}
        )
        for contender in contenders:
            result = {}

            # Find the title
            title = contender.find("span", {"itemprop": "name"})
            if title and title.text:
                result["title"] = title.text.replace("\n", "").strip()

            # Find link to main website
            links = contender.find_all("a", {"target": "_blank"})
            if not links:
                continue

            url = links[0].attrs.get("href")
            if not url:
                continue
            result["url"] = url

            # Get authors
            authors = contender.find("li", {"itemprop": "author"})
            if authors:
                result["credit"] = [
                    x.text.replace(",", "").strip()
                    for x in authors.find_all("span")
                    if x.text
                ]

            # Get tags (will supplement topics)
            tags = contender.find_all("div", {"class": "keyword-label"})
            if tags:
                result["tags"] = [
                    x.text.strip().lower().replace(" ", "-") for x in tags if x.text
                ]

            # Description
            desc = contender.find("td", {"class": "description"})
            desc = desc.find_next("div")
            if desc and desc.text:
                result["description"] = desc.text.replace("\n", "").strip()
            bot.info(f"Found record {result['url']}")
            self.results.append(result)

        return self.results

    def create(self, database=None, config_file=None, update=False):
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
                repo = get_parser(uid, allow_custom=False)

                # Test to see if singular GitHub or Gitlab
                if (
                    ("github" in repo.uid or "gitlab" in repo.uid)
                    and repo.uid.count("/") != 2
                    or ".html" in repo.uid
                ):
                    continue

                data = repo.get_metadata() or {}
                if not data:
                    continue
                result = update_nonempty(result, data)

            except NotImplementedError:
                continue

            # Add results that don't exist
            exists = client.exists(repo.uid)
            if not exists:
                client.add(repo.uid, data=result)
            elif exists and update:
                # rewrite defaults to false
                client.update(repo.uid, data=result)
