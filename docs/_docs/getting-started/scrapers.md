---
title: Scrapers
category: Getting Started
permalink: /getting-started/scrapers/index.html
order: 5
---

Scrapers support discovering software repositories from different resources
that might then be added via a core [parser](../parsers). By default, a scraper
will query for some number of latest updated entries. If you provide a query
string, it will be searched for that instead.

## How does it work?

It's very common to find software cross-referenced, meaning that you might find a GitHub
repository represented in a Journal of Open Software paper, or a random database of software having mentions of
both. In fact, we can look at these resources as databases that are regularly updated with
research software that we want to add from. Since the research software encyclopedia is 
optimized to be maintained as a repository flat-file "database" on version control (GitHub), 
we have chosen to honor version control software as our bases of truth. For example, although we might
find metadata in JoSS, since it's typically pointing back to code in a version control system,
we just use JoSS to find these repositories. If we find additional valuable metadata, however,
 (e.g., a DOI) we add this to the base GitHub or other version control record. 
We use this strategy as a best effort to not have redundancy in the representation of software repositories,
but still capture metadata that we need.

## Scrapers

The following scrapers are planned for development, depending on if an API is available,
and it includes links to repositories:

 - [The Journal of Open Source Software (JoSS)](#joss)
 - [bio.tools](#biotools)
 - [Hal Research Software Database](#hal)
 - [Research Software NL Dictionary](#researchsoftwarenl)


<a id="joss">
### Journal of Open Source Software

The Journal of Open Source Software is one of my favorite resources for new
software. Although the site has an RSS (atom) feed, you can't easily retrieve GitHub urls
from it, so instead we parse the main site, either for latest, or based on a search
query:

```bash
$ rse scrape joss
INFO:rse.main.scrapers.joss:Found repository: https://github.com/LiberTEM/LiberTEM
INFO:rse.main.scrapers.joss:Found repository: https://github.com/samhforbes/PupillometryR
INFO:rse.main.scrapers.joss:Found repository: https://github.com/Alcampopiano/hypothesize
INFO:rse.main.scrapers.joss:Found repository: https://github.com/BartoszBartmanski/StoSpa2
INFO:rse.main.scrapers.joss:Found repository: https://github.com/rgmyr/corebreakout
INFO:rse.main.scrapers.joss:Found repository: https://github.com/coljac/sensie
INFO:rse.main.scrapers.joss:Found repository: https://github.com/HajkD/LTRpred
INFO:rse.main.scrapers.joss:Found repository: https://github.com/mzy2240/ESA
INFO:rse.main.scrapers.joss:Found repository: https://github.com/KVSlab/turtleFSI.git
INFO:rse.main.scrapers.joss:Found repository: https://github.com/anmolter/XLUR
```

If you don't want to add repositories to the database (but just do a test run) add `--dry-run`

```bash
$ rse scrape --dryrun joss
```

You can also scrape based on a term of interest:

```bash
$ rse scrape --dryrun joss docker
```

<a id="within-python">
#### Within Python

And of course you can interact with a scraper from within Python! Either
of the following will work to get the joss scraper:

```python
from rse.main.scrapers import get_named_scraper
scraper = get_named_scraper('joss')
```

```python
from rse.main.scrapers import JossScraper
scraper = JossScraper()
```

And then you can either search for a term, or get the latest (on the front page)

```python
results = scraper.latest()
results = scraper.search("docker")
```

By default, the latest won't paginate (it would parse all of JoSS) but you
can force it to:

```python
results = scraper.latest(paginate=True)
```
A query search does paginate by default, as the results are likely to be smaller.
Finally, if you want to create the repos that you have (the ones that 
don't exist in the research software encyclopedia yet) just run create.
The results are returned above, but they are also saved to the client.

```python
scraper.create()
```

<a id="biotools">
### Bio.Tools

The [bio.tools](https://bio.tools) database is a rich source of scientific software,
specifically for biotools. It serves an [application pgogramming interface](https://biotools.readthedocs.io/en/latest/api_reference.html) that we can query with the Research Software Encyclopedia, making
it a good scraper. To scrape latest (does not have pagination), simply do:


```bash
$ rse scrape biotools
```

To do a dry run:

```bash
$ rse scrape --dry-run biotools
INFO:rse.main.scrapers.biotools:Found repository: https://github.com/smajidian/phaseme
INFO:rse.main.scrapers.biotools:Found repository: https://github.com/COVIDep/COVIDep
INFO:rse.main.scrapers.biotools:Found repository: https://github.com/NIB-SI/DiNAR
INFO:rse.main.scrapers.biotools:Found repository: https://github.com/reproducible-biomedical-modeling/Biosimulations
INFO:rse.main.scrapers.biotools:Found repository: https://github.com/Brazelton-Lab/seq-annot
INFO:rse.main.scrapers.biotools:Found repository: https://github.com/gevaertlab/BetaVAEImputation
INFO:rse.main.scrapers.biotools:Found repository: https://github.com/herrsalmi/FConverter
INFO:rse.main.scrapers.biotools:Found repository: https://github.com/yanzhanglab/Graph2GO
```

You can also search for a term (also using `--dry-run` if desired:

```bash
$ rse scrape --dry-run biotools docker
```

The [within python](#within-python) interaction is the same, except you need to
select the biotools named parser.

```python
from rse.main.scrapers import get_named_scraper
scraper = get_named_scraper('biotools')
```
```python
from rse.main.scrapers import BioToolsScraper
scraper = BioToolsScraper()
```

<a id='hal'>
### Hal Research Software Database

The [Hal Research Software Database](https://hal.archives-ouvertes.fr/) exposes a search API,
and the client here tries to search for a subset of software that have github somewhere
in the search (for latest). If you search for a term, although you will get more results,
it's less likely to find GitHub or GitLab.


```bash
$ rse scrape hal
```

To do a dry run:

```bash
$ rse scrape --dry-run hal
INFO:rse.main.scrapers.hal:Found repository: github.com/DreamCloud-Project/AMALTHEA-Microworkload-Generator
INFO:rse.main.scrapers.hal:Found repository: github.com/DreamCloud-Project/AMALTHEA-SimGrid
INFO:rse.main.scrapers.hal:Found repository: github.com/genotoul-bioinfo/dgenies
INFO:rse.main.scrapers.hal:Found repository: github.com/gijut/gnucash
INFO:rse.main.scrapers.hal:Found repository: github.com/DreamCloud-Project/McSim-Cycle-accurate-Xbar
INFO:rse.main.scrapers.hal:Found repository: github.com/DreamCloud-Project/McSim-TLM-NoC
INFO:rse.main.scrapers.hal:Found repository: github.com/DreamCloud-Project/McSim-Cycle-accurate-NoC
INFO:rse.main.scrapers.hal:Found repository: github.com/HEML/HEML
INFO:rse.main.scrapers.hal:Found repository: github.com/kkjawz/coref-ee
INFO:rse.main.scrapers.hal:Found repository: github.com/linbox-team/linbox
Found 10 results
```

You can also search for a term (also using `--dry-run` if desired:

```bash
$ rse scrape --dry-run hal docker
```

The [within python](#within-python) interaction is the same, except you need to
select the biotools named parser.

```python
from rse.main.scrapers import get_named_scraper
scraper = get_named_scraper('hal')
```
```python
from rse.main.scrapers import HalScraper
scraper = HalScraper()
```

<a id="researchsoftwarenl">
### Research Software Dictionary (NL)

The [Research Software Dictionary](https://research-software.nl/) is a dictionary
of software deployed by the Netherlands eScience Center that also provides a nice
application programming interface (API) that we can parse.

```bash
$ rse scrape rsnl
```

To do a dry run:

```bash
$ rse scrape --dry-run rsnl
INFO:rse.main.scrapers.rsnl:Found repository: https://github.com/3D-e-Chem/knime-kripodb
INFO:rse.main.scrapers.rsnl:Found repository: https://github.com/3D-e-Chem/knime-pharmacophore
INFO:rse.main.scrapers.rsnl:Found repository: https://github.com/3D-e-Chem/knime-plants
INFO:rse.main.scrapers.rsnl:Found repository: https://github.com/3D-e-Chem/knime-python-node-archetype
...
INFO:rse.main.scrapers.rsnl:Found repository: https://github.com/iomega/spec2vec
INFO:rse.main.scrapers.rsnl:Found repository: https://github.com/NLESC-JCER/linux_actions_runner
Found 149 results
```

The [within python](#within-python) interaction is the same, except you need to
select the biotools named parser.

```python
from rse.main.scrapers import get_named_scraper
scraper = get_named_scraper('rsnl')
```
```python
from rse.main.scrapers import RSNLScraper
scraper = RSNLScraper()
```
