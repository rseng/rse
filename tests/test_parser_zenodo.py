#!/usr/bin/env python
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import os
import sys
import pytest


def test_parser_zenodo(tmp_path):
    """Test the zenodo parser.
    """
    from rse.main.parsers import ZenodoParser

    for repo in [
        "10.5281/zenodo.1012531",
    ]:
        parser = ZenodoParser(repo)
        assert parser.uid == "zenodo/10.5281/zenodo.1012531"
        assert parser.summary()

    # Only test one get of data
    assert not parser.get_metadata()
    assert parser.get_metadata(require_repo=False)
    data = parser.export()
    for key in ["timestamp", "doi", "links", "metadata"]:
        assert key in data
