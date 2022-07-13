---
layout: post
title: "Snakemake"
date: 2020-07-26 08:30:46
author: "@vsoch"
annotate_criteria: https://rseng.github.io/software/repository/github/snakemake/snakemake/annotate-criteria/
annotate_taxonomy: https://rseng.github.io/software/repository/github/snakemake/snakemake/annotate-taxonomy/
categories:
- Software
---

This week for the sofware survey we are highlighting <a href="https://github.com/snakemake/snakemake" target="_blank">snakemake/snakemake</a>, a workflow manager for Python that makes it easy to create and run a workflow from a high performance computing environment
to a cloud provider.

<ul>
<li><a href="{{ page.annotate_criteria }}" target="_blank">Annotate the software criteria</a></li>
<li><a href="{{ page.annotate_taxonomy }}" target="_blank">Annotate the software taxonomy</a></li>
</ul>


or learn more about it in the following sections.

<!--more--> 

 - [What is snakemake?](#what-is)
 - [How do I cite it?](#cite)
 - [How do I contribute to the software survey](#contribute)
 - [Where can I learn more?](#learn-more)


<a id="what-is">
## What is snakemake?

From the [snakemake documentation](https://snakemake.readthedocs.io/en/stable/):

> The Snakemake workflow management system is a tool to create reproducible and scalable data analyses. Workflows are described via a human readable, Python based language. They can be seamlessly scaled to server, cluster, grid and cloud environments, without the need to modify the workflow definition. Finally, Snakemake workflows can entail a description of required software, which will be automatically deployed to any execution environment.

The great thing about Snakemake is that is empowers scientific programmers, many of which are comfortable with
Python, to create and execute workflows at scale. At the same time, you can store them in a GitHub repository.
And this shows in it's usage! Did you know that (as of the writing of this post) Snakemake gets about [3 new citations per week](https://badge.dimensions.ai/details/id/pub.1018944052)?

👉️ [snakemake documentation](https://snakemake.readthedocs.io/en/stable/) 


<a id="cite">
## How do I cite it?

See [this section of the documentation](https://snakemake.readthedocs.io/en/stable/project_info/citations.html) for more details on citation.

```
@article{10.1093/bioinformatics/bts480,
    author = {Köster, Johannes and Rahmann, Sven},
    title = "{Snakemake—a scalable bioinformatics workflow engine}",
    journal = {Bioinformatics},
    volume = {28},
    number = {19},
    pages = {2520-2522},
    year = {2012},
    month = {08},
    abstract = "{Summary: Snakemake is a workflow engine that provides a readable Python-based workflow definition language and a powerful execution environment that scales from single-core workstations to compute clusters without modifying the workflow. It is the first system to support the use of automatically inferred multiple named wildcards (or variables) in input and output filenames.Availability:http://snakemake.googlecode.com.Contact:johannes.koester@uni-due.de}",
    issn = {1367-4803},
    doi = {10.1093/bioinformatics/bts480},
    url = {https://doi.org/10.1093/bioinformatics/bts480},
    eprint = {https://academic.oup.com/bioinformatics/article-pdf/28/19/2520/819790/bts480.pdf},
}
```

<a id="getting-started">
## How do I get started?

If you want to get started with snakemake, here are some good links!

 - [Resources](https://snakemake.readthedocs.io/en/stable/#resources) including profiles for different environments, wrappers, and workflows.
 - [Getting Started Tutorial](https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html)
 - [Quick Tutorial](https://snakemake.readthedocs.io/en/stable/tutorial/short.html)
 - [Executor Tutorials](https://snakemake.readthedocs.io/en/stable/executor_tutorial/tutorial.html)


You can also post questions on the [GitHub issues board](https://github.com/snakemake/snakemake/issues).


<a id="contribute">
## How do I contribute to the software survey?

<ul>
<li><a href="{{ page.annotate_criteria }}" target="_blank">Annotate the software criteria</a></li>
<li><a href="{{ page.annotate_taxonomy }}" target="_blank">Annotate the software taxonomy</a></li>
</ul>

or read more about annotation [here]({{ site.baseurl }}/tutorials/annotate-your-software). You can clone the software repository to do
bulk annotation, or annotation any repository in the <a href="https://rseng.github.io/software/" target="_blank">software database</a>,
We want annotation to be fun, straight-forward, and easy, so we will be showcasing one repository to annotate per week.
If you'd like to request annotation of a particular repository (or addition to the software database)
please don't hesitate to [open an issue](https://github.com/rseng/software/issues) or even a pull request.

<a id="learn-more">
## Where can I learn more?

You might find these other resources useful:

 - [The Research Software Database](https://github.com/rseng/software) on GitHub
 - [RSEpedia Documentation](https://rseng.github.io/rse)
 - [Google Docs Manuscript](https://docs.google.com/document/d/1wDb0udH9OrFWrMBsAVb8RrUMCKKRHoyEep7yveJ1d0k/edit) you are invited to contribute to.
 - [Annotation Documentation for RSEpedia](https://rseng.github.io/rse/tutorials/annotation/)
 - [Annotation Tutorial in RSEng docs](https://rseng.github.io/rse/tutorials/annotation/)

For any resource, you are encouraged to give feedback and contribute!
