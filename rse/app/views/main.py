"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from flask import render_template

# from werkzeug import secure_filename
from rse.app.server import app, socketio
from rse.defaults import RSE_SOCKET_UPDATE_SECONDS

from threading import Thread, Event

# thread for updates
thread = Thread()
thread_stop_event = Event()


## Main Index View


@app.route("/")
def index():

    return render_template(
        "home/filesystem-index.html",
        database=app.client.database,
        criteria=app.client.list_criteria(),
        entries=app.client.list_taxonomy(),
    )


## Updating database rows


def update_database():
    """A function to be run at some interval to update the rse database listing
    """
    while not thread_stop_event.isSet():

        # The data sent to the table depends on the database
        if app.client.database == "filesystem":

            # Break into parser types and uid
            socketio.emit(
                "FSdatabase",
                {"rows": app.client.list(), "database": app.client.database},
                namespace="/update",
            )

        # sqlite or other relational
        else:
            socketio.emit(
                "RELdatabase",
                {"rows": app.client.list(), "database": app.client.database},
                namespace="/update",
            )

        socketio.sleep(RSE_SOCKET_UPDATE_SECONDS)


@socketio.on("deleterow", namespace="/table/action")
def delete_row(json):
    """a request to delete a particular row"""
    app.logger.debug("Received deletion request for %s", json.get("taskid"))
    taskid = json.get("taskid", "doesnotexist")
    was_deleted = app.client.clear(target=taskid, noprompt=True)
    socketio.emit(
        "deleterowcomplete",
        {"wasdeleted": was_deleted, "taskid": taskid},
        namespace="/table/action",
    )


@socketio.on("rerunrow", namespace="/table/action")
def rerun_row(json):
    """a request to re-run a particular task.
    """
    app.logger.debug("Received re-run request for %s", json.get("taskid"))
    taskid = json.get("taskid", "doesnotexist")
    was_rerun = app.client.rerun(taskid) is not None
    socketio.emit(
        "reruncomplete",
        {"wasrerun": was_rerun, "taskid": taskid},
        namespace="/table/action",
    )


@socketio.on("connect", namespace="/update")
def update_connect():
    # need visibility of the global thread object
    global thread
    app.logger.debug("Client connected")

    # Start the process to update the table
    app.logger.debug("Starting Thread")
    thread = socketio.start_background_task(update_database)


@socketio.on("disconnect", namespace="/update")
def update_disconnect():
    app.logger.debug("Client disconnected")
