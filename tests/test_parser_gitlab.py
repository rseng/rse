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


def test_parser_gitlab(tmp_path):
    """Test the gitlab parser.
    """
    from rse.main.parsers import GitLabParser

    for repo in [
        "singularityhub/gitlab-ci",
        "gitlab.com/singularityhub/gitlab-ci",
        "git@gitlab.com:singularityhub/gitlab-ci.git",
    ]:
        parser = GitLabParser(repo)
        assert parser.uid == "gitlab/singularityhub/gitlab-ci"
        assert parser.summary()

    # Only test one get of data
    assert parser.get_metadata()
    data = parser.export()
    for key in ["timestamp", "description", "web_url"]:
        assert key in data
