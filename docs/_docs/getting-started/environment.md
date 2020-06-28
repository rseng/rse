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
The default shell for an interactive client (defaults to ipython, then checks python, and bpython)

The default endpoint to retrieve criteria and taxonomy information. Defaults to `https://rseng.github.io/rseng/api`
to provide each of:

 - https://rseng.github.io/rseng/api/taxonomy/
 - https://rseng.github.io/rseng/api/criteria

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

### RSE_API_ENDPOINT

The endpoint to retrieve the taxonomy and criteria from. Defaults to `https://rseng.github.io/rseng/api`.

```bash
export RSE_API_ENDPOINT=https://rseng.github.io/another/api
```

### RSE_ISSUE_ENDPOINT

The repository to post criteria and taxonomy annotations to, via the static interface.
Defaults to `https://github.com/rseng/software`

```bash
export RSE_ISSUE_ENDPOINT=https://github.com/rseng/another
```

## RSE Dashboard

### RSE_URL_PREFIX

If you are running a server and want to add a prefix to the url, export
that:

```bash
export RSE_URL_PREFIX=/software
```

This is especially important if you are running `rse export` for GitHub
pages, as you'll need the url prefix to coincide with the GitHub pages repository
name.

### RSE_HOST

In the case that you are exporting content for GitHub pages, you'll want to export
`RSE_HOST` to be the hostname and port that you need. For example:

```bash
export RSE_HOST=https://rseng.github.io
```

## RSE Parsers

Each parser can maintain it's own namespace of environment variables. These
should be specified in the format `RSE_<PARSER>_<NAME>`

### RSE_GITHUB_TOKEN

To interact with GitHub repositories with reasonable API limits, it's recommended 
to set this environment variable, a personal access token or a GitHub actions 
`GITHUB_TOKEN`.

```bash
export RSE_GITHUB_TOKEN=1234...
```

## RSE_ZENODO_TOKEN

You can also provide a zenodo API token to increase limits for the Zenodo parser.

```bash
export RSE_ZENODO_TOKEN=1234...
```
