"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import flask
from flask_restful import Resource, Api
from rse.app.server import app


def list_repos(parser=None):
    """A shared function to list one or more repos, optionally for a parser,
       and return a json list to serialize to the api view
    """
    repos = []
    url = flask.request.host_url
    for i, repo in enumerate(app.client.list(parser)):
        repos.append(
            {
                "uid": repo[0],
                "html_url": "%sparser/%s" % (url, repo[0]),
                "api_url": "%sapi/repos/%s" % (url, repo[0]),
            }
        )
    return repos


class apiList(Resource):
    """display all tasks
    """

    def get(self):
        return list_repos()


class apiListParser(Resource):
    """display all tasks for an executor
    """

    def get(self, parser):
        return list_repos(parser)


class apiGet(Resource):
    """display a specific repo
    :param uid: id for a specific task
    """

    def get(self, uid):
        repo = app.client.get(uid)
        return repo.export()


class apiEndpoints(Resource):
    """show all API endpoints
    """

    def get(self):
        url = flask.request.host_url
        return {
            "/api": "%sapi" % url,
            "/api/repos": "%sapi/repos" % url,
            "/api/criteria": "%sapi/criteria" % url,
            "/api/taxonomy": "%sapi/taxonomy" % url,
            "/api/repos/<path:uid>": "%sapi/repos/<path:uid>" % url,
            "/api/repos/parser/<string:parser>": "%sapi/repos/parser/<string:parser>"
            % url,
        }


class apiGetCriteria(Resource):
    """display the listing of criteria
    """

    def get(self):
        return app.client.list_criteria()


class apiGetTaxonomy(Resource):
    """display the flattened taxonomy.
    """

    def get(self):
        return app.client.list_taxonomy()


api = Api(app)
api.add_resource(apiEndpoints, "/api")
api.add_resource(apiList, "/api/repos")
api.add_resource(apiGet, "/api/repos/<path:uid>")
api.add_resource(apiGetTaxonomy, "/api/taxonomy")
api.add_resource(apiGetCriteria, "/api/criteria")
api.add_resource(apiListParser, "/api/repos/parser/<string:parser>")
