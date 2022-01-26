"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.defaults import RSE_API_ENDPOINT
import requests
import logging
import sys

bot = logging.getLogger("rse.main.criteria")
parser_regex = "github"


def get_criteria():
    """Get criteria from the default endpoint."""
    response = requests.get(f"{RSE_API_ENDPOINT}/criteria/")
    if response.status_code != 200:
        sys.exit(f"Problem with getting {RSE_API_ENDPOINT}/criteria/")
    return response.json()["data"]
