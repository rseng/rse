---
title: Application Programming Interface
category: Getting Started
permalink: /getting-started/api/index.html
order: 8
---

Let's say that you have a container running, and it serves as a base to to serve
metadata for your research software encyclopedia. It runs an [interactive dashboard](../dashboard/)
and that's great, but you really need programmatic access to the repositories
taxonomy, and criteria. How might you do that?

## The Application Programming Interface

The dashboard also exposes a simple Restful API to the database! After you
start the dashboard:

```bash
$ rse start
```

If you look at the bottom of the table, there is a small link to view the tasks api.

![../img/api/dashboard.png](../img/api/dashboard.png)


## API Views

 - [Api Index (root)](#index)
 - [List Repositories](#list-repos)
 - [List Repositories by Parser](#list-parser)
 - [List Single Repository](#list-repo)
 - [List Criteria](#list-criteria)
 - [List Taxonomy](#list-taxonomy)


<a id="index">
### Index

**/api**

The first page you go to is the index, which shows the pattern for endpoints that exist.

![../img/api/root.png](../img/api/root.png)


<a id="list-repos">
###  List Repositories


**/api/repos**

You can quickly see a listing of all repositories in the encyclopedia:

![../img/api/repos.png](../img/api/repos.png)


<a id="list-parser">
###  List Repositories by Parser


**/api/repos/parser/[name]**

Or a listing based on the parser (e.g., GitHub)

![../img/api/parser.png](../img/api/parser.png)


<a id="list-repo">
### List Single Repository

**/api/repos/[uid]**

If you adjust the url (`/api/repos/<uid>`) to specify a particular repository, you'll see it's exported metadata:

![../img/api/repo.png](../img/api/repo.png)


<a id="list-criteria">
###  List Criteria

**/api/criteria**

You can also view a listing of all criteria:

![../img/api/criteria.png](../img/api/criteria.png)


<a id="list-taxonomy">
###  List Taxonomy

**/api/taxonomy**

or a flattened list of categories in the taxonomy:

![../img/api/taxonomy.png](../img/api/taxonomy.png)

If you'd like to see any other endpoints added, please [open an issue]({{ site.baseurl }}/{{ site.repo }}/issues).
