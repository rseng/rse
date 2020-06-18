"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from flask import render_template, request, redirect
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


@app.route("/annotate")
def annotate_repos(message=""):
    return render_template(
        "annotate/repos.html", database=app.client.database, message=message
    )


@app.route("/annotate-criteria", methods=["POST", "GET"])
def annotate_criteria():

    # If it's a post, update the annotation
    username = None
    if request.method == "POST":
        print("IN POST")
        update_criteria()

    # Username on GitHub is required for annotation lookup
    username = request.args.get("username", username)
    print("Username is %s" % username)
    if username in [None, ""]:
        return annotate_repos(
            message="Please provide your GitHub username above to start the annotation session."
        )

    # Get the first set of criteria
    last = None
    annotation_sets = []
    for repo, criteria in app.client.yield_criteria_annotation_repos(
        username=username, unseen_only=True
    ):
        if last is not None and last.uid != repo.uid:
            break
        last = repo
        annotation_sets.append((repo, criteria,))

    return render_template(
        "annotate/criteria.html",
        database=app.client.database,
        sets=annotation_sets,
        username=username,
    )


@app.route("/annotate-taxonomy")
def annotate_taxonomy():
    return render_template("annotate/taxonomy.html", database=app.client.database)


# Helper Functions


def update_criteria():

    repo_id = None
    updates = {}

    for key in request.form.keys():
        for value in request.form.getlist(key):
            if key.startswith("radio-RSE-"):
                updates[key.replace("radio-", "", 1)] = value
            elif key == "repo_uid":
                repo_uid = value
            elif key == "username":
                username = value

    # Do the update for each criteria
    repo = app.client.get(repo_id)
    for key, response in updates.items():
        print(f"Updating {repo} {key} with {response}")
        repo.update_criteria(key, username, response)

    # The filesystem database saves at the end
    if hasattr(repo, "save_criteria"):
        repo.save_criteria()

    # Relational saves the database item
    else:
        app.client.db.update(repo)
