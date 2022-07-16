"""

Copyright (C) 2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import pytest

from rse.main.scrapers import get_importer


def test_get_unknown_import():
    with pytest.raises(SystemExit):
        get_importer("noodles")


def test_google_sheet_import(tmp_path):
    """
    Test google-sheet import
    """
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsPmEWUg8Tr1ZoYTcQ0kTdsCrVskQveSuwfdEHaktHtQG693O4DHQrZotoFd5dXCLAciykAYNf-RSz/pub?gid=0&single=true&output=csv"
    importer = get_importer("google-sheet")
    results = importer.scrape(url)
    assert len(results) == 9

    # Assert we have required fields
    for result in results:
        for key in ["title", "url", "description"]:
            assert key in result and result[key]
