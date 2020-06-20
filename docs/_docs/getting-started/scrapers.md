---
title: Scrapers
category: Getting Started
permalink: /getting-started/scrapers/index.html
order: 5
---

Scrapers support discovering software repositories from different resources
that might then be added via a core [parser](../parsers).

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

 - The Journal of Open Source Software (JoSS)
 - bio.tools
 - Hal Research Software Database
 - Software Dictionary: https://research-software.nl/

**under development**

You might next want to learn about the interactive [dashboard]({{ site.baseurl }}/getting-started/dashboard/).
