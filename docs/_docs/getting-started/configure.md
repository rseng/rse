---
title: Configuration
category: Getting Started
permalink: /getting-started/configure/index.html
order: 2
---

Configuration is optional, and will (if desired) allow you to define a custom
database for your install. For many settings, you can either set or update them via
the command line client with `rse config`, or set [environment variables](../environment/) 
at runtime (or in your bash profile) for one off changes to default configurations.
When you first install rse and run `rse init` an rse.ini (the configuration
file for a software repository) will be created in the present folder,
and the database stored here.

```bash
$ ls
└── rse.ini
```

## Databases

Rseng uses some backend database to keep track of your software repository.
While the filesystem database (default) is suitable for most, and also fits nicely
within a GitHub repository, for those users that want, you can also specify
a more robust database ranging from sqlite to postgres. As a reminder, 
you would need to [install]({{ site.baseurl }}/install/)
the sqlalchemy dependencies for this, you need to do:

```bash
$ pip install rse[database]
```

and then to set the database to be sqlite, make sure you are in the directory
of your config file (or specify it with `--config_file`) and then run:

```bash
$ rse config --database sqlite
INFO:rse.client:Configuration saved with database sqlite
```

More details on database types are included below.


### Filesystem

The default database, the `filesystem` that doesn't require any additional dependencies,
is considered a dummy or testing database. It will, by default, generate a "database"
folder in your software repository:

```bash
$ tree -L 1
├── database
└── rse.ini
```

STOPPED HERE - need to develop software repository class

Once you run an parser, a subfolder will be created based on the name of
the parser (e.g., github) and within that folder, one json file will be created
per repository parsed:

```bash
$ tree $HOME/.rse
/home/vanessa/.rse
├── rse.ini
├── dashboard.log
└── database
    └── github
        ├── singularityhub
        └── vsoch
```

If you've changed your database and want to update it back to be the filesystem,
just run:

```bash
$ rse config --database filesystem
```

### Sqlite

Sqlite is a reasonable choice for most use cases, as it appropriately scales enough for
the general user, and allows for relational database-like functionality without
needing anything other than permission to write a file. If you want to set a sqlite
database as default from the command line, just run:

```bash
$ rse config --database sqlite
Configuration saved with database sqlite
```

And the default sqlite database will be at a location in your QME_HOME ($HOME/.rse)
in a file `QME_DATABASE_STRING`, which defaults to `rse.db` and can be set in 
the [environment](../environment/). You can set this to be more permanent by setting
it in your config file like this:

```bash
$ rse config --database sqlite://mydatabase.db
Configuration saved with database sqlite://mydatabase.db
```

would then create `$HOME/.rse/mydatabase.db` as the default sqlite database. Again,
if you need to "one off" this setting for a particular environment or command,
you can export `QME_DATABASE` and `QME_DATABASE_STRING`:

```bash
export QME_DATABASE=sqlite
export QME_DATABASE_STRING=mydatabase.db
```

to achieve the same result. When you have an sqlite database (akin to another
relational) your `rse ls` listing will have the command added, making
it much more useful:

```bash
$ rse ls
Database: sqlite
1  shell-9d38a272-e0d1-4027-8c93-382a8fcbd290	ls
2  shell-9f593e88-3ecd-4e14-adf5-d615f2262f24	whoami
3  shell-513a4c2f-13be-4a9c-8f97-8ae3bcc8049b	singularity --help
```


### Postgres and MySql

Both postgres and mysql have the same format for the database string, albeit
they interact with different databases, and have different prefixes. Here is
how you can set either:

```bash
$ rse config --database mysql+pymysql://username:password@host/dbname
# or
$ rse config --database postgresql://username:password@host/dbname
```

This is **strongly** recommended to be set as an environment variable so that you don't
write credentials to a text file. So you instead might do this:

```bash
$ rse config --database mysql+pymysql
# or
$ rse config --database postgresql
```

and then export the rest via an environment variable:

```bash
export RSE_DATABASE_STRING=username:password@host/dbname
```

which would work for both types.

If you want some help with your configuration, please don't be afraid to [reach out](https://github.com/{{ site.repo }}/issues). You might next want to see how [environment variables]({{ site.baseurl }}/getting-started/environment/) can further customize your usage of rse.
