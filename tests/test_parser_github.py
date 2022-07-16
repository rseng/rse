"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""


def test_parser_github(tmp_path):
    """
    Test the github parser.
    """
    from rse.main.parsers import GitHubParser

    for repo in [
        "singularityhub/sregistry",
        "github.com/singularityhub/sregistry",
        "git@github.com:singularityhub/sregistry.git",
    ]:
        parser = GitHubParser(repo)
        assert parser.uid == "github/singularityhub/sregistry"
        assert parser.summary()

    # Only test one get of data
    assert parser.get_metadata()
    data = parser.export()
    for key in ["timestamp", "url", "html_url"]:
        assert key in data


def test_org_repos(tmp_path):
    """
    Test the github parser to retrieve org repos.
    """
    from rse.main.parsers import GitHubParser

    parser = GitHubParser()
    data = parser.get_org_repos("ropensci", paginate=False)
    assert len(data) == 100
