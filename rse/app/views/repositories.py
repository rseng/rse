"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from flask import render_template
from rse.app.server import app


## Repository Views


@app.route("/repository/<path:uid>")
def repository_view(uid):

    repo = app.client.get(uid)

    if repo.parser.name == "github":
        skips = ["owner", "organization", "node_id"]
        return render_template(
            "parsers/github.html",
            repo=repo.load(),
            database=app.client.database,
            skips=skips,
        )
