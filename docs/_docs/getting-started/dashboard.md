---
title: Dashboard
category: Getting Started
permalink: /getting-started/dashboard/index.html
order: 5
---

## Dashboard

The dashboard can be started with `rse start`

```bash
$ rse start
INFO:rse.main:Database: filesystem
INFO:engineio.server:Server initialized for threading.
Research Software Encyclopedia: running on http://127.0.0.1:5000
```

By default, it will deploy the dashboard to [localhost:5000](http://localhost:5000).
The dashboard will show a cards view of your repositories, with an option to filter
by GitHub tags.

![img/dashboard/topics.png](../img/dashboard/topics.png)

When the application starts, it will initialize the encyclopedia and database,
so you should either be in the same directory as a `rse.ini` (the root of the
repository that you want to annotate) or define the variable in either of the
following ways:

```bash
$ rse start --config_file /path/to/rse.ini
```

or 

```bash
export RSE_CONFIG_FILE=/path/to/rse.ini
```

The interface is not currently hugely useful, but is going to be developed to allow for an
annotation session.


### Customization

You can customize the port with `--port`:

```bash
$ rse start --port 8000
```

For development, you'll need to add `--debug`:

```bash
$ rse start --debug
```

Development mode means that the views (front and back) refresh with changes,
which won't happen otherwise. 

### Python Interaction

The server can also be run by calling the start function directly, and providing
a client to a research encyclopedia:

```python
from rse.app.server import start
from rse.main import Encyclopedia

client = Encyclopedia(config_file="/path/to/rse.ini")
start(debug=True, client=client, port=5000)
```

You can also call from the server script directly:

```bash
$ python rse/app/server.py
```

This would be equivalent to calling the start command with defaults.

### Secret Key

The server requires a secret key, and scripts have been provided
to generate one for you. For example we can run:

```bash
$ rse generate-key
8RI$5rs|bIP=e#,,ZJ^iTAG$/Ax5hl@@HHg}fdt:hGB^MI)=NY
```

and export this to `RSE_SERVER_KEY` on your host:

```bash
export RSE_SERVER_KEY=8RI$5rs|bIP=e#,,ZJ^iTAG$/Ax5hl@@HHg}fdt:hGB^MI)=NY
```

and it will be detected in the environment. You could also do:

```bash
$ export RSE_SERVER_KEY=$(rse generate-key)
```

If you use the research software encyclopedia in a container, you should provide the key as an environment variable on start.

```bash
$ docker run -it --entrypoint /bin/bash --env RSE_SERVER_KEY=mysecretkey --rm -p 5000:5000 quay.io/vanessa/rse 
```

### Logging

If you want to look at server logs for the dashboard, they will be printed
by defualt to the root of your repository alongside the `rse.ini` file in a file called `dashboard.log`:

```bash
$ cat dashboard.log 
Starting Thread
2020-05-16 16:13:29,555 - rse.app.server - DEBUG - Client connected
2020-05-16 16:13:29,555 - rse.app.server - DEBUG - Starting Thread
2020-05-16 16:13:33,644 - rse.app.server - DEBUG - Client connected
```

You might next want to browse [tutorials]({{ site.baseurl }}/tutorials/) available.
