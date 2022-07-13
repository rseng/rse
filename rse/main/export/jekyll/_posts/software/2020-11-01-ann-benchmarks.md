---
layout: post
title: "ann-benchmarks"
date: 2020-11-01
author: "@tabakg"
annotate_criteria: https://rseng.github.io/software/repository/github/erikbern/ann-benchmarks/annotate-criteria/
annotate_taxonomy: https://rseng.github.io/software/repository/github/erikbern/ann-benchmarks/annotate-taxonomy/
categories:
- Software
---

Today's post is all about benchmarking. We'll focus on <a href="https://github.com/erikbern/ann-benchmarks" target="_blank">erikbern/ann-benchmarks</a>, which is project used to evaluate approximate nearest neighbor searches (ANN).

What is ANN? In many applications we want to solve the nearest neighbor problem -- given some point in the dataset, what are other points closest to it? For example, if you are listening to one song in a dataset and want recommendations for similar songs, you might want to look at its nearest neighbors! People have found ways to speed up nearest neighbor searches using approximation methods, which are often good enough. Hence, 'Approximate Nearest Neighbors'!

<br>

![{{ site.baseurl }}/assets/img/posts/showcase/qps.png]({{ site.baseurl }}/assets/img/posts/showcase/qps.png)

<br>

Do you have an opinion? We encourage you to contribute to the [research software encyclopedia](https://rseng.github.io/rse/tutorials/annotation/) and annotate the respository:

<ul>
<li><a href="{{ page.annotate_criteria }}" target="_blank">Annotate the software criteria</a></li>
<li><a href="{{ page.annotate_taxonomy }}" target="_blank">Annotate the software taxonomy</a></li>
</ul>

otherwise, keep reading!

<!--more--> 

 - [What is ann-benchmarks?](#what-is)
 - [How do I cite it?](#cite)
 - [How do I get started?](#getting-started)
 - [How do I contribute to the software survey](#contribute)
 - [Where can I learn more?](#learn-more)


<a id="what-is">
## What is ann-benchmarks?

Benchmarking approximate algorithms has unique difficulties. Usually when benchmarking a deterministic algorithm, we might only care about how long it takes on particular hardware. Or if we're doing data science, we don't care much about how long it takes -- only on some statistical measures instead! But for ANN we need a combination of these two points of view.

ann-benchmarks invents a way to combine these two points of view: It plots queries per second (roughly speed) versus recall (roughly how many of the nearest neighbors did we get). This will vary depending on hardware, so a number of leading algorithms have been placed in Docker containers, along with a handful of representative data sets (different algorithms can perform differently depending on features of the data set, like its dimension).

The only dependencies are Python 3.6 and Docker. Just clone and install the package. Running it is easy (although running all algorithms on all data sets can take days!). You can configure a YAML file to specify datasets. An example invocation:

```bash
python run.py --dataset glove-100-angular
```

In this case, the script would run all algorithms on the 'glove-100-angular' dataset.

#### Why is it useful?

This repo is very nice for those interested in benchmarking ANN on their data with their own hardware given how easy it is to use. It also represents best practices in reproducibility by running each algorithm in a container. I hope we will see this trend continue for benchmarking other algorithms (especially approximate algorithms that have unique challenges)!

Also check out ann-benchmarks.com for an extensive list of results across the various algorithms and datasets used.

<a id="cite">
## How do I cite it?

There is an accompanying paper paper, which you can cite using:

```
@inproceedings{aumuller2017ann,
  title={ANN-benchmarks: A benchmarking tool for approximate nearest neighbor algorithms},
  author={Aum{\"u}ller, Martin and Bernhardsson, Erik and Faithfull, Alexander},
  booktitle={International Conference on Similarity Search and Applications},
  pages={34--49},
  year={2017},
  organization={Springer}
}
```

<a id="getting-started">
## How do I get started?
 
 - [README Documentation](https://github.com/erikbern/ann-benchmarks#Install) is always a good place to start.
 - [ann-benchmarks.com](http://ann-benchmarks.com) is the main site.

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
