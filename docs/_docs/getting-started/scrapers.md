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
 - bio.tools
 - Hal Research Software Database
 - Software Dictionary: https://research-software.nl/


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

And of course you can interact with a scraper from within Python! Either
of the following will work to get the joss scraper:

```python
from rse.main.scrapers import get_named_scraper
scraper = get_named_scraper('joss')
```

```python
from rse.main.scrapers import JossScraper
scraper = JossScraper('joss')
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

**under development**
