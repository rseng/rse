---
title: Environment
category: Getting Started
permalink: /getting-started/environment/index.html
order: 3
---

## RSE Global Environment
The following environment variables can be set to determine runtime behavior.

### RSE_CONFIG_FILE
If set, identify your Research Software Encyclopedia by way of the path to this file.

```
export RSE_CONFIG_FILE=/path/to/rse.ini
```

By doing so, you can interact with your software repository via `rse.ini` without
needing to specify `--config_file`.

### RSE_WORKERS
the number of multiprocessing workers to use. This value is set to be 2*2nproc + 1 if not set.

### RSE_SHELL
the default shell for an interactive manager (defaults to ipython, then checks python, and bpython)

### RSE_DATABASE

the database to use. For example, you can specify just `filesystem` or `sqlite`, or `postgresql` or `mysql+pymysql` 
for mysql. For the last three, you can optionally specify `RSE_DATABASE_STRING` to include a particular
set of credentials needed for access, and this is recommended over providing the values into the rse.ini config
for a software repository. To export a particular database type, here are examples:

```bash
export RSE_DATABASE=mysql+pymysql
export RSE_DATABASE=postgresql
export RSE_DATABASE=filesystem
export RSE_DATABASE=sqlite
```

For more permanent settings, you should use the [configure client](../configure/) instead.

### RSE_DATABASE_STRING

If you have a custom string for a database or file, you can specify it with `RSE_DATABASE_STRING`.
For example, sqlite might look like this:

```bash
export RSE_DATABASE_STRING=mydatabase.db
```
and would create `mydatabase.db` in your software repository root. For a relational database with
username, password, and tables, you would export a full string:

```bash
export RSE_DATABASE_STRING=username:password@host/dbname
```

See [database setup](../configure/index.html#databases) for more details.

### RSE_LOG_LEVEL

If you want to set the logging level from the environment, set `RSE_LOG_LEVEL` to 
one of "WARNING" "DEBUG" "INFO" "CRITICAL" "ERROR" or "FATAL". For example, to silence
most all messages, we might set it to fatal:

```bash
export RSE_LOG_LEVEL=FATAL
```

You can override the environment default by way of using the `--log_level` flag:

```bash
$ rse --log_level INFO get
```

If you set an environment level that is not one of the choices, it will default
to using info. If you provide an inccorect value to `--log_level` you will be asked
to run the command again and choose from the valid choices.

### RSE_SOCKET_UPDATE_SECONDS

If you are using the dashboard (which uses web sockets) this is the number of
seconds to update it. This basically will update the dashboard table
with the content of your Qme Database.

You might next want to browse [commands]({{ site.baseurl }}/getting-started/commands/) that can
be run with rse.

## RSE Parsers

Each parser can maintain it's own namespace of environment variables. These
should be specified in the format `RSE_<PARSER>_<NAME>`

### RSE_GITHUB_TOKEN

To interact with GitHub repositories, you need to set this environment variable,
a personal access token or a GitHub actions `GITHUB_TOKEN` if run during a GitHub workflow.
If you don't set it, you'll get this message when trying to add a repository:

```bash
RSE_GITHUB_TOKEN is required
```
