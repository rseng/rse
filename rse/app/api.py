"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import flask
from flask_restful import Resource, Api
from rse.app.server import app
from rse.defaults import RSE_URL_PREFIX, RSE_HOST


def list_repos(parser=None):
    """A shared function to list one or more repos, optionally for a parser,
       and return a json list to serialize to the api view
    """
    repos = []
    url = (RSE_HOST or flask.request.host_url) + RSE_URL_PREFIX
    for i, repo in enumerate(app.client.list(parser)):
        repos.append(
            {
                "uid": repo[0],
                "html_url": "%srepository/%s" % (url, repo[0]),
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
        return repo.load()


class apiEndpoints(Resource):
    """show all API endpoints
    """

    def get(self):
        url = (RSE_HOST or flask.request.host_url) + RSE_URL_PREFIX
        return {
            "%sapi" % RSE_URL_PREFIX: "%sapi" % url,
            "%sapi/repos" % RSE_URL_PREFIX: "%sapi/repos" % url,
            "%sapi/criteria" % RSE_URL_PREFIX: "%sapi/criteria" % url,
            "%sapi/taxonomy" % RSE_URL_PREFIX: "%sapi/taxonomy" % url,
            "%sapi/repos/<path:uid>" % RSE_URL_PREFIX: "%sapi/repos/<path:uid>" % url,
            "%sapi/repos/parser/<string:parser>"
            % RSE_URL_PREFIX: "%sapi/repos/parser/<string:parser>"
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
api.add_resource(apiEndpoints, "%sapi" % RSE_URL_PREFIX)
api.add_resource(apiList, "%sapi/repos" % RSE_URL_PREFIX)
api.add_resource(apiGet, "%sapi/repos/<path:uid>" % RSE_URL_PREFIX)
api.add_resource(apiGetTaxonomy, "%sapi/taxonomy" % RSE_URL_PREFIX)
api.add_resource(apiGetCriteria, "%sapi/criteria" % RSE_URL_PREFIX)
api.add_resource(apiListParser, "%sapi/repos/parser/<string:parser>" % RSE_URL_PREFIX)
