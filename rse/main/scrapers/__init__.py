"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from .biotools import BioToolsScraper
from .hal import HalScraper
from .joss import JossScraper
from .molssi import MolssiScraper
from .rsnl import RSNLScraper
from .ropensci import ROpenSciScraper
from .imperial import ImperialCollegeLondonScraper
import re


def get_named_scraper(name, config=None):
    """get a named scraper, meaning determining based on name"""
    scraper = None
    if re.search("(joss|journal of open source software)", name, re.IGNORECASE):
        scraper = JossScraper()
    elif re.search("(biotool|bio[.]tool)", name, re.IGNORECASE):
        scraper = BioToolsScraper()
    elif re.search("hal", name, re.IGNORECASE):
        scraper = HalScraper()
    elif re.search("(researchsoftwarenl|rsnl)", name, re.IGNORECASE):
        scraper = RSNLScraper()
    elif re.search("ropensci", name, re.IGNORECASE):
        scraper = ROpenSciScraper()
    elif re.search("molssi", name, re.IGNORECASE):
        scraper = MolssiScraper()
    elif re.search("imperial", name, re.IGNORECASE):
        scraper = ImperialCollegeLondonScraper()

    if not scraper:
        raise NotImplementedError(f"There is no matching scraper for {name}")

    scraper.config = config
    return scraper
