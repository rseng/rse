---
title: Containers
category: Getting Started
permalink: /getting-started/containers/index.html
order: 7
---

It's very likely that you might want to use rse in a headless environment
where you don't have the ability to install a ton of custom dependencies.
This is the ideal use case for containers! We will walk through the basic
build and usage for the automated Docker build here, and then how
to pull the container down to Singularity for cluster usage.

## Docker

If you want to build the container on your own, you can do that as follows:

```bash
$ git clone git@github.com:rseng/rse
cd rse
$ docker build -t quay.io/vanessa/rse .
```

Note that you can also just pull the container - there is an automated build
for it at Quay.io at [quay.io/vanessa/rse](https://quay.io/repository/vanessa/rse?tab=tags).

```bash
$ docker pull quay.io/vanessa/rse
```
