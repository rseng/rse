"""

Copyright (C) 2020-2023 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import logging
import sys

import requests

from rse.defaults import RSE_API_ENDPOINT

bot = logging.getLogger("rse.main.taxonomy")
parser_regex = "github"


def get_taxonomy():
    """Get taxonomy from the default endpoint."""
    response = requests.get(f"{RSE_API_ENDPOINT}/taxonomy/")
    if response.status_code != 200:
        sys.exit(f"Problem with getting {RSE_API_ENDPOINT}/taxonomy/")
    taxonomy = response.json()["data"]
    # Sort by the ordering
    return sorted(taxonomy, key=lambda i: i["path"])
