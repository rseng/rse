"""

Copyright (C) 2022-2023 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import csv
import logging
import sys
from io import StringIO

import requests

from rse.utils.urls import get_user_agent

from .csv import CSVImporter

bot = logging.getLogger("rse.main.import.google-sheet")


class GoogleSheetImporter(CSVImporter):
    name = "googlesheet"

    def scrape(self, args, **kwargs):
        """
        The main function to perform the scrape to import and return results.
        """
        # We expect a listing of urls
        if isinstance(args, str):
            args = [args]

        # Each arg should be a URL
        for url in args:
            response = requests.get(url, headers={"User-Agent": get_user_agent()})
            if response.status_code != 200:
                sys.exit(f"Issue parsing {url}: {response.reason}")

            # Parse csv
            f = StringIO(response.text)
            reader = csv.reader(f, delimiter=",")
            rows = [x for x in reader if x]
            if not rows:
                sys.exit(f"Sheet {url} does not have any rows.")
            self.results += self.parse_rows(rows)
            return self.results
