"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from .joss import JossScraper
import re


def get_named_scraper(name, config=None):
    """get a named scraper, meaning determining based on name
    """
    scraper = None
    if re.search("(joss|journal of open source software)", name, re.IGNORECASE):
        scraper = JossScraper()

    if not scraper:
        raise NotImplementedError(f"There is no matching scraper for {name}")

    scraper.config = config
    return scraper
