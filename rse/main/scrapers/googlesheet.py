"""

Copyright (C) 2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.utils.urls import get_user_agent
from rse.main.parsers import CustomParser, get_parser
from rse.utils.strings import update_nonempty
import logging
import requests
import csv
from io import StringIO

from .base import ScraperBase

bot = logging.getLogger("rse.main.import.google-sheet")


def read_rows(filepath, newline="", delim=","):
    """
    read in the data rows of a csv file.
    """
    # Read in the entire membership counts
    with open(filepath, newline=newline) as infile:
        reader = csv.reader(infile, delimiter=delim)
        data = [row for row in reader]
    return data


class GoogleSheetImporter(ScraperBase):

    name = "googlesheet"

    def scrape(self, args):
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
                bot.exit(f"Issue parsing {url}: {response.text}")

            # Parse csv
            f = StringIO(response.text)
            reader = csv.reader(f, delimiter=",")
            rows = [x for x in reader if x]
            if not rows:
                bot.exit(f"Sheet {url} does not have any rows.")

            header = [x.lower() for x in rows.pop(0)]
            for required in ["title", "url", "description"]:
                if required not in header:
                    bot.exit(f"Sheet {url} is missing required field {required}.")

            for row in rows:
                repo = {value: row[i] for i, value in enumerate(header) if value}
                complete = True
                for required in ["title", "url", "description"]:
                    if not repo[required]:
                        complete = False
                if not complete:
                    continue

                # If we have topics, ensure to parse
                if "tags" in repo:
                    repo["tags"] = [x.strip() for x in repo["tags"].split(",")]
                bot.info("Found software record: %s" % repo["url"])
                self.results.append(repo)
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
                repo = get_parser(uid)
                data = repo.get_metadata()
                result = update_nonempty(result, data)

            # Or as custom entry
            except NotImplementedError:
                # Base UID based on title
                repo = CustomParser(result["title"])
                repo.set_metadata(
                    title=result["title"],
                    url=result["url"],
                    description=result["description"],
                )

            # Add results that don't exist
            exists = client.exists(repo.uid)
            if not exists:
                client.add(repo.uid, data=result)
            elif exists and update:
                # rewrite defaults to false
                client.update(repo.uid, data=result)
