"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from flask_socketio import SocketIO
from flask import Flask

from rse.logger import bot
from rse.defaults import RSE_HOSTNAME

import logging
import os


class ResearchSoftwareServer(Flask):
    def __init__(self, *args, **kwargs):
        super(ResearchSoftwareServer, self).__init__(*args, **kwargs)


app = ResearchSoftwareServer(__name__)
app.config.from_object("rse.app.config")

# turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

from rse.app.views import *
from rse.app.api import *


def start(
    port=5000, debug=True, client=None, host=None, level="DEBUG", disable_annotate=False
):
    """Start can be invoked when this file is executed (see __main__ below)
    or used as a function to programmatically start a server. If started
    via rse start, we can add the encyclopedia client to the server.
    If you want to change the hostname, set the environment variable
    RSE_HOSTNAME or set on command line with rse start.
    """
    host = host or RSE_HOSTNAME
    bot.info(f"Research Software Encyclopedia: running on http://{host}:{port}")

    # If the user doesn't specify a queue, use default
    if not client:
        from rse.main import Encyclopedia

        client = Encyclopedia()

    # Customize the logger to log to the app folder
    file_handler = logging.FileHandler(os.path.join(client.config_dir, "dashboard.log"))
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(getattr(logging, level))

    # Add the queue to the server
    app.client = client
    app.disable_annotate = disable_annotate
    socketio.run(app, port=port, debug=debug, host=host)


# This is how the command line version will run
if __name__ == "__main__":
    start()
