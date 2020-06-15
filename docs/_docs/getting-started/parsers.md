---
title: Parsers
category: Getting Started
permalink: /getting-started/parsers/index.html
order: 4
---

A parser is a client that is able to take a namespaced unique resource identifier (uri)
and extract metadata for software using it. For example, a GitHub parser will
know how to take a GitHub url address and extract metadata about the URL
while using it. While most parsers are interacted with by way of a SoftwareRespository
handler (meaning that the user has created a local database of software to interact with)
the parsers can also be interacted with externally to this structure. This
document will overview parsers, and provide examples for interacting with each.

 - [Base Parser](#base)
 - [GitHub Parser](#github)

## The Parser Base

All executors should be derived from the [ParserBase](https://github.com/rse/rse/blob/master/rse/main/parsers/base.py) class that will ensure that each one exposes the needed functions. Each parser will also have it's own view under [app/templates](https://github.com/rse/rse/tree/master/rse/app/templates) that renders a page specific to it for the dashboard (under development). You should reference the class to see the functions that are required and conditions for each.

## Parsers

<a id="base">
### Base

Each parser must expose the following metadata:

 - **timestmap**: when the parsing was run
 - **name**: the name of the parser (e.g., github)
 - **uid**: the unique id within the parser space (e.g., a GitHub unique resource identifier)

The only metadata shown on the table (front) page of the dashboard is these common attributes.

<a id="github">
### GitHub

The "github" parser is intended to treat a GitHub url as a software repository,
and uses the GitHub API to extract metadata for it.  A `RSE_GITHUB_TOKEN` is required
to be exported to the environment. We define the following
additional metadata.


Example usage of the parser outside of the Encyclopedia might look like the following.
If you want to instantiate an empty parser (not associated with a software repository)
you can do that as follows:

```python
from rse.main.parsers import GitHubParser
parser = GitHubParser()
```

However, it's more likely that you want to parse a specific repository. That works
like any of the following:


```python
from rse.main.parsers import GitHubParser
parser = GitHubParser('singularityhub/sregistry')
parser = GitHubParser('github.com/singularityhub/sregistry')
parser = GitHubParser('git@github.com:singularityhub/sregistry.git')
```
In all three cases, the uri is parsed to be in the format `<parser>/<identifier>`,
and for GitHub that means `github/<owner>/<repository>` and we would see:

```
parser.uid
# github/singularityhub/sregistry
```

Note that you can also use the get_parser function to retrieve the parser, but you
are required to have "github" somewhere in the string:

```python
from rse.main.parsers import get_parser
parser = get_parser('github.com/singularityhub/sregistry')
```

You can also get a named parser:

```python
from rse.main.parsers import get_named_parser
parser = get_named_parser('github')
```

And then you can set a unique resource identifier after the fact:

```python
from rse.main.parsers import get_named_parser 
parser = get_named_parser('github')

parser.set_uri('github/singularityhub/sregistry')
parser.uid
#'github/singularityhub/sregistry'
```

Once the identifier is loaded, you can parse updated metadata for it.
Note that this requires a `RSENG_GITHUB_TOKEN` to be set in the environment.
You can then get the repository-level metadata about the software repository:

```python
data = parser.get_metadata()
{'id': 99180575,
 'node_id': 'MDEwOlJlcG9zaXRvcnk5OTE4MDU3NQ==',
 'name': 'sregistry',
 'full_name': 'singularityhub/sregistry',
 'private': False,
 'owner': {'login': 'singularityhub',
  'id': 24552884,
  'node_id': 'MDEyOk9yZ2FuaXphdGlvbjI0NTUyODg0',
  'avatar_url': 'https://avatars1.githubusercontent.com/u/24552884?v=4',
  'gravatar_id': '',
  'url': 'https://api.github.com/users/singularityhub',
  'html_url': 'https://github.com/singularityhub',
  'followers_url': 'https://api.github.com/users/singularityhub/followers',
  'following_url': 'https://api.github.com/users/singularityhub/following{/other_user}',
  'gists_url': 'https://api.github.com/users/singularityhub/gists{/gist_id}',
  'starred_url': 'https://api.github.com/users/singularityhub/starred{/owner}{/repo}',
  'subscriptions_url': 'https://api.github.com/users/singularityhub/subscriptions',
  'organizations_url': 'https://api.github.com/users/singularityhub/orgs',
  'repos_url': 'https://api.github.com/users/singularityhub/repos',
  'events_url': 'https://api.github.com/users/singularityhub/events{/privacy}',
  'received_events_url': 'https://api.github.com/users/singularityhub/received_events',
  'type': 'Organization',
  'site_admin': False},
 'html_url': 'https://github.com/singularityhub/sregistry',
 'description': 'server for storage and management of singularity images',
 'fork': False,
 'url': 'https://api.github.com/repos/singularityhub/sregistry',
 'forks_url': 'https://api.github.com/repos/singularityhub/sregistry/forks',
 'keys_url': 'https://api.github.com/repos/singularityhub/sregistry/keys{/key_id}',
 'collaborators_url': 'https://api.github.com/repos/singularityhub/sregistry/collaborators{/collaborator}',
 'teams_url': 'https://api.github.com/repos/singularityhub/sregistry/teams',
 'hooks_url': 'https://api.github.com/repos/singularityhub/sregistry/hooks',
 'issue_events_url': 'https://api.github.com/repos/singularityhub/sregistry/issues/events{/number}',
 'events_url': 'https://api.github.com/repos/singularityhub/sregistry/events',
 'assignees_url': 'https://api.github.com/repos/singularityhub/sregistry/assignees{/user}',
 'branches_url': 'https://api.github.com/repos/singularityhub/sregistry/branches{/branch}',
 'tags_url': 'https://api.github.com/repos/singularityhub/sregistry/tags',
 'blobs_url': 'https://api.github.com/repos/singularityhub/sregistry/git/blobs{/sha}',
 'git_tags_url': 'https://api.github.com/repos/singularityhub/sregistry/git/tags{/sha}',
 'git_refs_url': 'https://api.github.com/repos/singularityhub/sregistry/git/refs{/sha}',
 'trees_url': 'https://api.github.com/repos/singularityhub/sregistry/git/trees{/sha}',
 'statuses_url': 'https://api.github.com/repos/singularityhub/sregistry/statuses/{sha}',
 'languages_url': 'https://api.github.com/repos/singularityhub/sregistry/languages',
 'stargazers_url': 'https://api.github.com/repos/singularityhub/sregistry/stargazers',
 'contributors_url': 'https://api.github.com/repos/singularityhub/sregistry/contributors',
 'subscribers_url': 'https://api.github.com/repos/singularityhub/sregistry/subscribers',
 'subscription_url': 'https://api.github.com/repos/singularityhub/sregistry/subscription',
 'commits_url': 'https://api.github.com/repos/singularityhub/sregistry/commits{/sha}',
 'git_commits_url': 'https://api.github.com/repos/singularityhub/sregistry/git/commits{/sha}',
 'comments_url': 'https://api.github.com/repos/singularityhub/sregistry/comments{/number}',
 'issue_comment_url': 'https://api.github.com/repos/singularityhub/sregistry/issues/comments{/number}',
 'contents_url': 'https://api.github.com/repos/singularityhub/sregistry/contents/{+path}',
 'compare_url': 'https://api.github.com/repos/singularityhub/sregistry/compare/{base}...{head}',
 'merges_url': 'https://api.github.com/repos/singularityhub/sregistry/merges',
 'archive_url': 'https://api.github.com/repos/singularityhub/sregistry/{archive_format}{/ref}',
 'downloads_url': 'https://api.github.com/repos/singularityhub/sregistry/downloads',
 'issues_url': 'https://api.github.com/repos/singularityhub/sregistry/issues{/number}',
 'pulls_url': 'https://api.github.com/repos/singularityhub/sregistry/pulls{/number}',
 'milestones_url': 'https://api.github.com/repos/singularityhub/sregistry/milestones{/number}',
 'notifications_url': 'https://api.github.com/repos/singularityhub/sregistry/notifications{?since,all,participating}',
 'labels_url': 'https://api.github.com/repos/singularityhub/sregistry/labels{/name}',
 'releases_url': 'https://api.github.com/repos/singularityhub/sregistry/releases{/id}',
 'deployments_url': 'https://api.github.com/repos/singularityhub/sregistry/deployments',
 'created_at': '2017-08-03T02:17:03Z',
 'updated_at': '2020-06-05T18:21:34Z',
 'pushed_at': '2020-06-05T18:21:35Z',
 'git_url': 'git://github.com/singularityhub/sregistry.git',
 'ssh_url': 'git@github.com:singularityhub/sregistry.git',
 'clone_url': 'https://github.com/singularityhub/sregistry.git',
 'svn_url': 'https://github.com/singularityhub/sregistry',
 'homepage': 'https://singularityhub.github.io/sregistry',
 'size': 13251,
 'stargazers_count': 52,
 'watchers_count': 52,
 'language': 'JavaScript',
 'has_issues': True,
 'has_projects': True,
 'has_downloads': True,
 'has_wiki': True,
 'has_pages': True,
 'forks_count': 32,
 'mirror_url': None,
 'archived': False,
 'disabled': False,
 'open_issues_count': 23,
 'license': {'key': 'mpl-2.0',
  'name': 'Mozilla Public License 2.0',
  'spdx_id': 'MPL-2.0',
  'url': 'https://api.github.com/licenses/mpl-2.0',
  'node_id': 'MDc6TGljZW5zZTE0'},
 'forks': 32,
 'open_issues': 23,
 'watchers': 52,
 'default_branch': 'master',
 'permissions': {'admin': True, 'push': True, 'pull': True},
 'temp_clone_token': '',
 'allow_squash_merge': True,
 'allow_merge_commit': True,
 'allow_rebase_merge': True,
 'delete_branch_on_merge': False,
 'organization': {'login': 'singularityhub',
  'id': 24552884,
  'node_id': 'MDEyOk9yZ2FuaXphdGlvbjI0NTUyODg0',
  'avatar_url': 'https://avatars1.githubusercontent.com/u/24552884?v=4',
  'gravatar_id': '',
  'url': 'https://api.github.com/users/singularityhub',
  'html_url': 'https://github.com/singularityhub',
  'followers_url': 'https://api.github.com/users/singularityhub/followers',
  'following_url': 'https://api.github.com/users/singularityhub/following{/other_user}',
  'gists_url': 'https://api.github.com/users/singularityhub/gists{/gist_id}',
  'starred_url': 'https://api.github.com/users/singularityhub/starred{/owner}{/repo}',
  'subscriptions_url': 'https://api.github.com/users/singularityhub/subscriptions',
  'organizations_url': 'https://api.github.com/users/singularityhub/orgs',
  'repos_url': 'https://api.github.com/users/singularityhub/repos',
  'events_url': 'https://api.github.com/users/singularityhub/events{/privacy}',
  'received_events_url': 'https://api.github.com/users/singularityhub/received_events',
  'type': 'Organization',
  'site_admin': False},
 'network_count': 32,
 'subscribers_count': 10}
```

You might next want to learn about the interactive [dashboard]({{ site.baseurl }}/getting-started/dashboard/).
