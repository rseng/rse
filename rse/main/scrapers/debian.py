"""

Copyright (C) 2020-2023 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import logging
import re

from rse.main.parsers import get_parser
from rse.utils.strings import update_nonempty

from .base import ScraperBase

bot = logging.getLogger("rse.main.scrapers.debian-med")


class DebianMedScraper(ScraperBase):
    name = "debian-med"
    matchstring = "(debian|debianmed|debian-med)"

    def __init__(self, query=None, **kwargs):
        super().__init__(query)
        self.baseurl = "https://blends.debian.org/med/tasks"

    def latest(self, paginate=False, delay=0.0):
        return self.scrape(paginate=paginate, delay=delay)

    def search(self, query, paginate=True, delay=0.0):
        return self.scrape(paginate=paginate, delay=delay, query=query)

    def scrape(self, paginate=False, delay=None, query=""):
        """
        A shared function to scrape software from debian-med
        """
        soup = self.soupify(self.baseurl)

        contenders = soup.find_all("a", href=True)
        for contender in contenders:
            # Each link to a subpage has a name, id, and href that are the same
            name = contender.attrs.get("name")
            identifier = contender.attrs.get("id")
            href = contender.attrs.get("href")
            if not name or (name != identifier != href):
                continue

            page = self.baseurl + "/" + name
            bot.info(f"Debian scraper looking at page {page}")
            page_soup = self.soupify(page)

            # Find tables, one project per table
            projects = page_soup.find_all("table", {"class": "project"})

            for project in projects:
                # Require a Github or gitlab link
                link = None
                for x in project.find_all("a"):
                    if re.search("(github|gitlab)", x.attrs.get("href", "")):
                        link = x.attrs.get("href")
                        break

                if not link:
                    continue

                # parse title
                title = project.find("div", {"class": "pkgname"})
                title = title.text.replace("\t", "").replace("\n", "").strip()
                description = (
                    project.find("div", {"class": "pkgdesc"})
                    .text.replace("\n", " ")
                    .strip()
                )

                result = {"url": link, "title": title, "description": description}

                # Do we have authors / publication?
                pub = project.find("span", {"class": "title"})
                if pub:
                    pub = pub.find("a")
                    if pub:
                        doi = pub.attrs.get("href")
                        if doi:
                            result["doi"] = doi
                bot.info(f"Found result for {result['url']}")
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

            # Don't allow custom for the time being
            except Exception as exc:
                bot.warning(exc)
                continue

            # Add results that don't exist
            exists = client.exists(repo.uid)

            # Cut out early if not going to add
            if exists and not update:
                continue

            data = repo.get_metadata() or {}
            if not data:
                continue
            result = update_nonempty(result, data)

            if not exists:
                client.add(repo.uid, data=result)
            elif exists and update:
                # rewrite defaults to false
                client.update(repo.uid, data=result)
