"""

Copyright (C) 2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main.parsers import GitHubParser
import logging
import requests

from .base import ScraperBase

bot = logging.getLogger("rse.main.scrapers.ropensci")


class ROpenSciScraper(ScraperBase):

    name = "ropensci"
    matchstring = "ropensci"

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

    def read_registry(self):
        """
        Read the registry file to create a lookup of repos based on GitHub URL.
        """
        lookup = {}
        response = requests.get(
            "https://raw.githubusercontent.com/ropensci/roregistry/gh-pages/registry.json"
        ).json()
        for entry in response.get("packages", []):
            # This is the GitHub URL
            url = entry.get("github")
            if not url:
                continue
            lookup[url] = entry
        return lookup

    def get_registry_topics(self, meta):
        """
        Given a metadata entry from the registry lookup, parse and return topics
        """
        topics = [x.strip() for x in meta.get("keywords", "").split(",") if x.strip()]
        if meta.get("ropensci_category"):
            topics += [meta.get("ropensci_category")]
        return topics

    def scrape(self, paginate=False, delay=None):
        """
        A shared function to scrape a set of repositories. Since the JoSS
        pages for a search and the base are the same, we can use a shared
        function.
        """
        # This serves as 1: a lookup, and 2: to find non ropensci repos!
        lookup = self.read_registry()

        # Full GitHub urls that we expect to find!
        names = set(lookup.keys())

        parser = GitHubParser()
        repos = parser.get_org_repos("ropensci", paginate=paginate, delay=delay)

        for entry in repos:

            # We determine belonging based on the github url
            if entry["html_url"] not in names:
                bot.info("Skipping repository: %s" % entry["html_url"])
                continue

            meta = lookup[entry["html_url"]]

            # Get topics from R metadata
            topics = self.get_registry_topics(meta)
            names.remove(entry["html_url"])
            if "topics" not in entry:
                entry["topics"] = []
            entry["topics"] += topics

            # Add a description if missing
            if not entry.get("description") and meta.get("description"):
                entry["description"] = meta["description"]

            bot.info("Adding repository: %s" % entry["html_url"])
            self.results.append(parser.parse_github_repo(entry))

        # If paginate is True, we intend to add ALL repos, so check those still remaining
        # E.g., there are repos in other orgs that won't be found above
        if paginate and names:
            for name in names:

                parser = GitHubParser(uid=name)
                # Topics will be added here!
                entry = parser.get_metadata()
                meta = lookup[name]

                # Add a description if missing
                if not entry.get("description") and meta.get("description"):
                    entry["description"] = meta["description"]
                entry["topics"] += self.get_registry_topics(meta)
                bot.info("Adding repository: %s" % entry["html_url"])
                self.results.append(entry)

        return self.results

    def create(self, database=None, config_file=None, **kwargs):
        """
        After a scrape (whether we obtain latest or a search query) we
        run create to create software repositories based on results.
        """
        from rse.main import Encyclopedia

        client = Encyclopedia(config_file=config_file, database=database)
        for result in self.results:
            uid = result["html_url"].split("//")[-1]

            # Add results that don't exist
            if not client.exists(uid):
                client.add(uid, data=result)
