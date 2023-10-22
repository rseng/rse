"""

Copyright (C) 2020-2023 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import os
import sys

import requests

from rse.utils.urls import get_user_agent


class ScraperBase:
    """
    A scraper base exists get new records from a resource.
    """

    name = "base"

    def __init__(self, query=None):
        """create a scraper. if a query term is provided, do search. Otherwise
        do a query for latest.
        """
        self.query = query
        self.results = []

    def latest(self, paginate=True, delay=0.0):
        """The scraper should expose a function to populate self.results with
        some number of latest entries.
        """
        raise NotImplementedError

    def search(self, paginate=True, delay=0.0):
        """
        The scraper should expose a function to populate self.results with
        a listing based on matching a search criteria.
        """
        raise NotImplementedError

    def create(self, uri, **kwargs):
        """
        After a scrape (whether we obtain latest or a search query) we
        run create to create software repositories based on results.
        """
        raise NotImplementedError

    def clean_uid(self, uid):
        """
        Try to clean a GitHub URL i a blob/tree is provided.
        """
        if "tree" in uid:
            uid = uid.split("tree", 1)[0]
        elif "blob" in uid:
            uid = uid.split("blob", 1)[0]

        # Do we have a GitHub pages address?
        if "github.io" in uid:
            uid = "github/%s/%s" % (
                uid.split(".")[0],
                [x for x in uid.split("/") if x][-1],
            )
        return uid

    def soupify(self, url, data=None, content_type="html.parser"):
        """
        Return url parsed with beautiful soup.
        """
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            sys.exit("BeautifulSoup is required. pip install rse[scraper].")

        response = requests.get(
            url, data=data, headers={"User-Agent": get_user_agent()}
        )
        if response.status_code != 200:
            sys.exit(f"Unable to retrieve {self.name} listing")

        return BeautifulSoup(response.text, content_type)

    def get_setting(self, key, default=None):
        """
        Get a setting, meaning that we first check the environment, then
        the config file, and then (if provided) a default.
        """
        # First preference to environment
        envar = ("RSE_%s_%s" % (self.name, key)).upper()
        envar = os.environ.get(envar)
        if envar is not None:
            return envar

        # Next preference to config setting
        parser = "scraper.%s" % self.name

        # Parsers instantiated separate from database won't have config
        if not hasattr(self, "config"):
            return default
        if parser not in self.config.config:
            return default
        if key in self.config.config[parser]:
            return self.config.get(parser, key)
        return default

    def summary(self):
        return "[scraper][%s][%s]" % (self.name, len(self.results))
