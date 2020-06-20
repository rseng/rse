---
title: Installation
category: Installation
permalink: /install/index.html
order: 1
---


## Install

QueueMe can be installed natively (python 3 recommended) with pip:

```bash
pip install rse
```

or via conda-forge:

```bash
conda install --channel conda-forge rse
```

or you can clone and install from source:

```bash
$ git clone https://github.com/vsoch/rse
$ cd rse
$ python setup.py install
```

or

```bash
$ pip install -e .
```

When you have installed rse, there will be an executable "rse"
placed in your bin folder:

```bash
which rse
/home/vanessa/anaconda3/bin/rse
```

and you should be able to run the executable and see the usage. However,
the basic install will not install a small number of extra dependencies needed
for a more robust (even sqlite) database (requires sqlalchemy) or a web interface
(requires Flask). To install these, the recommended install is to do:

```bash
pip install rse[database]
pip install -e .[database]
```

If you want to install the web interface, you'll need flask and some extras.
These can be installed with "app":

```bash
pip install rse[app]
pip install -e .[app]
```

if you want to use the scrapers, you need to install beautiful soup:

```bash
pip install rse[scraper]
pip install -e .[scraper]
```

or just install all dependencies:

```bash
pip install rse[all]
pip install -e .[all]
```

If you have any questions or issues, please [open an issue](https://github.com/{{ site.repo }}/issues).
