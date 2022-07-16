"""

Copyright (C) 2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import pytest


@pytest.mark.parametrize(
    "title, uid",
    [
        ["Research / Acoustic Indices", "custom/research/acoustic-indices"],
        ["Acoustic Indices", "custom/acoustic-indices"],
        ["Adobe audition", "custom/adobe-audition"],
        ["Anabat insight", "custom/anabat-insight"],
        ["Animal Sound Identifier", "custom/animal-sound-identifier"],
        ["ANIMAL-SPOT", "custom/animal-spot"],
        ["ARTWARP", "custom/artwarp"],
        ["Audacity", "custom/audacity"],
    ],
)
def test_parser_custom(title, uid, tmp_path):
    """
    Test a custom parser
    """
    from rse.main.parsers import CustomParser

    parser = CustomParser(title)
    assert parser.uid == uid
    assert parser.summary()
    assert parser.uid.count("custom") == 1

    # Test changing the parser name
    parser = CustomParser(title, namespace="research")
    assert parser.uid.startswith("research")
