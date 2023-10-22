"""

Copyright (C) 2020-2023 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import csv
import logging
import os
import sys

from rse.main.parsers import CustomParser, get_parser
from rse.utils.strings import update_nonempty

from .base import ScraperBase

bot = logging.getLogger("rse.main.import.csv")


def read_rows(filepath, newline=None, delim=None):
    """
    read in the data rows of a csv file.
    """
    newline = newline or ""
    delim = delim or ","

    # Read in the entire membership counts
    with open(filepath, newline=newline) as infile:
        reader = csv.reader(infile, delimiter=delim)
        data = [row for row in reader]
    return data


class CSVImporter(ScraperBase):
    name = "csv"

    def scrape(self, args, **kwargs):
        """
        The main function to perform the local "scrape" to return the csv
        """
        delim = kwargs.get("delim")
        newline = kwargs.get("newline")

        # should add ccustom args here
        # We expect a listing of paths
        if isinstance(args, str):
            args = [args]

        # Each arg should be a URL
        for sheet in args:
            if not os.path.exists(sheet):
                bot.info(f"{sheet} does not exist.")
                continue
            bot.info(f"Reading sheet {sheet}")
            rows = read_rows(sheet, delim=delim, newline=newline)
            if not rows:
                bot.warning(f"Sheet {sheet} does not have any rows.")
                continue
            self.results += self.parse_rows(rows)
        return self.results

    def parse_rows(self, rows):
        """
        Shared function to parse rows.
        """
        data = []
        if not rows:
            return data

        # Prepare based on header
        header = [x.lower() for x in rows.pop(0)]
        for required in ["title", "url", "description"]:
            if required not in header:
                sys.exit(f"Sheet is missing required field {required}.")

        for row in rows:
            repo = {value: row[i] for i, value in enumerate(header) if value}
            complete = True
            for required in ["title", "url", "description"]:
                if not repo[required]:
                    bot.warning("Row {row} is not complete, missing field {required}.")
                    complete = False
            if not complete:
                continue

            # If we have topics, ensure to parse
            if "tags" in repo:
                repo["tags"] = [x.strip() for x in repo["tags"].split(",")]
            bot.info("Found software record: %s" % repo["url"])
            data.append(repo)
        return data

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
            repo = get_parser(uid)
            data = repo.get_metadata() or {}

            # Empty or malformed repository
            if not data and repo.name == "custom":
                repo = CustomParser(result["title"])
                repo.set_metadata(
                    title=result["title"],
                    url=result["url"],
                    description=result["description"],
                )

            elif not data:
                bot.warning(f"Skipping malformed entry {uid}")
                continue
            result = update_nonempty(result, data)

            # Add results that don't exist
            exists = client.exists(repo.uid)
            if not exists:
                client.add(repo.uid, data=result)
            elif exists and update:
                # rewrite defaults to false
                client.update(repo.uid, data=result)
