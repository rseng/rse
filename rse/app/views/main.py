"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from flask import render_template
from rse.app.server import app
from rse.defaults import RSE_URL_PREFIX

## Main Index View


@app.route("/")
def index():

    return render_template(
        "home/filesystem-index.html",
        repos=app.client.list(),
        database=app.client.database,
        criteria=app.client.list_criteria(),
        entries=app.client.list_taxonomy(),
        url_prefix=RSE_URL_PREFIX,
        enable_annotate=not app.disable_annotate,
    )
