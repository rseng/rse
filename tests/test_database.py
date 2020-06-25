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


@pytest.mark.parametrize("database", ["filesystem", "sqlite"])
def test_parsers_filesystem(tmp_path, database):
    """test each parser with the filesystem database.
    """
    from rse.main import Encyclopedia

    config_dir = os.path.join(str(tmp_path), "software")
    os.mkdir(config_dir)
    config_file = os.path.join(config_dir, "rse.ini")

    enc = Encyclopedia(config_file=config_file, generate=True, database="database")

    # Each uid should map to a parser
    uids = [["github", "github.com/singularityhub/sregistry"]]
    for i, parts in enumerate(uids):

        parser = parts[0]
        uid = parts[1]
        repo = enc.get_or_create(uid)

        assert repo.parser.name == parser
        assert repo.filename == os.path.join(
            enc.config_dir, "database", repo.uid, "metadata.json"
        )
        assert repo.summary()

        # repo.load includes the file dump, the upper level keys should be same
        content = repo.load()
        for key in ["parser", "uid", "url", "data"]:
            assert key in content

        # repo.export includes the executor specific data
        data = repo.export()
        assert "timestamp" in data


@pytest.mark.parametrize("database", ["filesystem", "sqlite"])
def test_filesystem(tmp_path, database):
    """Test loading and using a queue with the filesystem database.
    """
    from rse.main import Encyclopedia

    config_dir = os.path.join(str(tmp_path), "software")
    os.mkdir(config_dir)
    config_file = os.path.join(config_dir, "rse.ini")

    # System exit if doesn't exist
    with pytest.raises(SystemExit):
        enc = Encyclopedia(config_file=config_file)

    enc = Encyclopedia(config_file=config_file, generate=True, database=database)
    assert enc.config.configfile == config_file

    assert os.path.exists(config_dir)
    assert enc.config_dir == config_dir
    assert enc.config.configfile == os.path.join(enc.config_dir, "rse.ini")
    assert enc.database == database
    assert enc.db.database == database
    if database == "filesystem":
        assert enc.db.data_base == os.path.join(config_dir, "database")

    # Test list, empty without anything
    assert not enc.list()

    # Add a repo
    repo = enc.add("github.com/singularityhub/sregistry")
    assert len(enc.list()) == 1

    # enc.get should return last repo, given no id
    lastrepo = enc.get()
    assert lastrepo.uid == repo.uid

    # Summary
    enc.summary()
    enc.summary("github.com/singularityhub/sregistry")
    enc.analyze("github.com/singularityhub/sregistry")
    enc.analyze_bulk()

    # Clean up a specific repo (no prompt)
    enc.clear(repo.uid, noprompt=True)
    assert len(enc.list()) == 0
    enc.clear(noprompt=True)
    assert not enc.list()

    # Get the taxonomy or criteria
    enc.list_taxonomy()
    enc.list_criteria()
