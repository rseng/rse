"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from flask import render_template
from rse.app.server import app
from rse.defaults import RSE_URL_PREFIX, RSE_HOST

import flask

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


@app.route("%ssearch" % RSE_URL_PREFIX)
def search():
    repos = []
    url = RSE_HOST + RSE_URL_PREFIX or flask.request.host_url + RSE_URL_PREFIX
    for i, name in enumerate(app.client.list()):
        repo = app.client.get(name[0])
        repos.append(
            {
                "uid": repo.uid,
                "description": repo.description,
                "url": repo.url,
                "html_url": "%srepository/%s" % (url, repo.uid),
                "api_url": "%sapi/repos/%s" % (url, repo.uid),
            }
        )
    return render_template(
        "search.html",
        repos=repos,
        database=app.client.database,
        url_prefix=RSE_URL_PREFIX,
    )
