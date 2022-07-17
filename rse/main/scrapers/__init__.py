"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from .ascl import AsclScraper
from .biotools import BioToolsScraper
from .hal import HalScraper
from .joss import JossScraper
from .molssi import MolssiScraper
from .rsnl import RSNLScraper
from .ropensci import ROpenSciScraper
from .imperial import ImperialCollegeLondonScraper
from .googlesheet import GoogleSheetImporter
import re
import sys

scrapers = [
    AsclScraper,
    BioToolsScraper,
    HalScraper,
    JossScraper,
    MolssiScraper,
    RSNLScraper,
    ROpenSciScraper,
    ImperialCollegeLondonScraper,
]


def get_importer(name):
    """
    Get an importer by name. Designed to support additional ones.
    An importer is technically a kind of scraper.
    """
    importer = None
    if name.lower() == "google-sheet":
        importer = GoogleSheetImporter()
    if not importer:
        sys.exit(f"Importer {name} is not known.")
    return importer


def get_named_scraper(name, config=None):
    """
    Get a named scraper, meaning determining based on name
    """
    scraper = None
    for ScraperClass in scrapers:
        if re.search(ScraperClass.matchstring, name, re.IGNORECASE):
            scraper = ScraperClass()
            break

    if not scraper:
        raise NotImplementedError(f"There is no matching scraper for {name}")

    scraper.config = config
    return scraper
