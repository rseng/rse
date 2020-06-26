"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from flask import render_template, request, redirect
from rse.app.server import app
from rse.defaults import RSE_URL_PREFIX, RSE_ISSUE_ENDPOINT
import random

## Repository Views


@app.route("%srepository/<path:uid>" % RSE_URL_PREFIX)
def repository_view(uid):

    # Obtain the repository and load the data.
    repo = app.client.get(uid)
    repo.parser.load(repo.data)

    if repo.parser.name == "github":
        skips = ["owner", "organization", "node_id"]
        return render_template(
            "parsers/github.html",
            repo=repo.load(),
            database=app.client.database,
            url_prefix=RSE_URL_PREFIX,
            skips=skips,
        )
    elif repo.parser.name == "gitlab":
        avatar = repo.parser.get_avatar()
        return render_template(
            "parsers/gitlab.html",
            repo=repo.load(),
            url_prefix=RSE_URL_PREFIX,
            database=app.client.database,
            avatar=avatar,
        )


@app.route("%sannotate" % RSE_URL_PREFIX)
def annotate_repos(message=""):
    return render_template(
        "annotate/repos.html",
        database=app.client.database,
        message=message,
        url_prefix=RSE_URL_PREFIX,
    )


@app.route("%sannotate-criteria" % RSE_URL_PREFIX, methods=["POST", "GET"])
def annotate_criteria():

    # If it's a post, update the annotation
    username = None
    if request.method == "POST":
        username = update_criteria()

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
        url_prefix=RSE_URL_PREFIX,
    )


@app.route("%srepository/<path:uid>/annotate-criteria" % RSE_URL_PREFIX)
def annotate_static_criteria(uid):

    # Get criteria / annotation set for specific repository
    username = request.args.get("username")
    repo = app.client.get(uid)
    criteria = app.client.list_criteria()

    return render_template(
        "annotate/criteria-static.html",
        database=app.client.database,
        sets=criteria,
        repo=repo,
        username=username,
        issue_endpoint=RSE_ISSUE_ENDPOINT,
        url_prefix=RSE_URL_PREFIX,
    )


@app.route("%srepository/<path:uid>/annotate-taxonomy" % RSE_URL_PREFIX)
def annotate_static_taxonomy(uid):

    # Get criteria / annotation set for specific repository
    username = request.args.get("username")
    repo = app.client.get(uid)

    # If we don't have a color lookup, make one
    if not hasattr(app, "taxonomy"):
        app.taxonomy = generate_taxonomy(app)

    return render_template(
        "annotate/taxonomy-static.html",
        database=app.client.database,
        sets=app.taxonomy,
        repo=repo,
        username=username,
        issue_endpoint=RSE_ISSUE_ENDPOINT,
        url_prefix=RSE_URL_PREFIX,
    )


@app.route("%sannotate-taxonomy" % RSE_URL_PREFIX, methods=["GET", "POST"])
def annotate_taxonomy():

    # If we don't have a color lookup, make one
    if not hasattr(app, "taxonomy"):
        app.taxonomy = generate_taxonomy(app)

    # If it's a post, update the annotation
    username = None
    if request.method == "POST":
        username = update_taxonomy()

    # Username on GitHub is required for annotation lookup
    username = request.args.get("username", username)
    print("Username is %s" % username)
    if username in [None, ""]:
        return annotate_repos(
            message="Please provide your GitHub username above to start the annotation session."
        )

    # Generator for repos that need annotation based on username
    generator = app.client.yield_taxonomy_annotation_repos(username, unseen_only=True)

    # Return the taxonomy with one repo, until we run out
    try:
        repo = next(generator)
        print(repo)
        return render_template(
            "annotate/taxonomy.html",
            database=app.client.database,
            taxonomy=app.taxonomy,
            repo=repo,
            username=username,
            url_prefix=RSE_URL_PREFIX,
        )

    except StopIteration as exc:
        return annotate_repos(
            message="You have already annotated taxonomy items for all the repos!"
        )


# Helper Functions


def generate_taxonomy(app):

    taxonomy = app.client.list_taxonomy()

    # Update the color list with existing colors (consistency)
    colors = {}
    for item in taxonomy:
        colors[item["name"]] = item["color"]

    # Add parents to the lookup
    colors["Software to directly conduct research"] = "darkblue"
    colors["General software"] = "darkgoldenrod"
    colors["Software to support research"] = "darkgreen"
    colors["Incidentally used for research"] = "darkmagenta"
    colors["Used for research but not explicitly for it"] = "darkslateblue"
    colors["Domain-specific software"] = "darkcyan"
    colors["Explicitly for research"] = "mediumpurple"

    # Generate a color for each unique entry
    for entry in taxonomy:
        parts = [x.strip() for x in entry["path"].split(">>")]
        colorlist = []
        for part in parts:
            colorlist.append(colors[part])
        entry["colors"] = colorlist
    return taxonomy


def update_criteria():

    updates = {}
    repo_uid = request.form.get("repo_uid")
    username = request.form.get("username")
    for key in request.form.keys():
        for value in request.form.getlist(key):
            if key.startswith("radio-RSE-"):
                updates[key.replace("radio-", "", 1)] = value

    # Do the update for each criteria
    repo = app.client.get(repo_uid)
    for key, response in updates.items():
        print(f"Updating {repo} {key} with {response}")
        repo.update_criteria(key, username, response)

    # The filesystem database saves at the end
    app.client.save_criteria(repo)

    return username


def update_taxonomy():

    uids = []
    repo_uid = request.form.get("repo_uid")
    username = request.form.get("username")
    for key in request.form.keys():
        for value in request.form.getlist(key):
            if key.startswith("RSE-taxonomy"):
                uids.append(key)

    # Do the update for each criteria
    repo = app.client.get(repo_uid)
    print(f"Updating {repo} with {uids}")
    app.client.save_taxonomy(repo, username, uids)
    return username
