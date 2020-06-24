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

**Primary Parsers**

Primary parsers are the core parsers to create records in the database, and generally
this means version control systems where software is stored.

 - [Base Parser](#base)
 - [GitHub Parser](#github)
 - [GitLab parser](#gitlab)
 - [Zenodo Parser](#zenodo)


For the parsers above, those with version controlled code are considered sources of
truth. For parsers like Zenodo, we look for a GitHub or Gitlab URL, and add an entry
to the database given that we have one. The user is free to use the Zenodo Parser
outside of the rse to bypass this requirement.


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
and uses the GitHub API to extract metadata for it.  A `RSE_GITHUB_TOKEN` is suggested
to be exported to the environment to increase your API limits, but not required.

#### Example Usage

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

You can also get a named parser, and then you can set a unique resource
identifier after the fact:

```python
from rse.main.parsers import get_named_parser
parser = get_named_parser('github')
parser.set_uid('github/singularityhub/sregistry')
parser.uid
#'github/singularityhub/sregistry'
```

Once the identifier is loaded, you can parse updated metadata for it.
Note that you can optionally export an `RSE_GITHUB_TOKEN` in the environment
to increase your API limit for bulk operations (recommended).
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

<a id="gitlab">
### GitLab

The "gitlab" parser is intended to treat a GitLab url as a software repository,
and uses the GitLab API to extract metadata for it.  A `RSE_GITLAB_TOKEN` is suggested
to be exported to the environment to increase your API limits, but not required. You
can generate one at your profile [here](https://gitlab.com/profile/personal_access_tokens).

#### Example Usage

Example usage of the parser outside of the Encyclopedia might look like the following.
If you want to instantiate an empty parser (not associated with a software repository)
you can do that as follows:

```python
from rse.main.parsers import GitLabParser
parser = GitLabParser()
```

However, it's more likely that you want to parse a specific repository. That works
like any of the following:


```python
from rse.main.parsers import GitLabParser
parser = GitLabParser('singularityhub/gitlab-ci')
parser = GitLabParser('gitlab.com/singularityhub/gitlab-ci')
parser = GitLabParser('git@gitlab.com:singularityhub/gitlab-ci')
```
In all three cases, the uri is parsed to be in the format `<parser>/<identifier>`,
and for GitLab that means `gitlab/<owner>/<repository>` and we would see:

```
parser.uid
# gitlab/singularityhub/gitlab-ci
```

Note that you can also use the get_parser function to retrieve the parser, but you
are required to have "gitlab" somewhere in the string:

```python
from rse.main.parsers import get_parser
parser = get_parser('gitlab.com/singularityhub/gitlab-ci')
```

You can also get a named parser, and then you can set a unique resource identifier after the fact:


```python
from rse.main.parsers import get_named_parser
parser = get_named_parser('gitlab')
parser.set_uid('singularityhub/gitlab-ci')
parser.uid
# gitlab/singularityhub/gitlab-ci
```

Once the identifier is loaded, you can parse updated metadata for it.
Note that this requires a `RSE_GITHUB_TOKEN` to be set in the environment.
You can then get the repository-level metadata about the software repository:

```python
data = parser.get_metadata()
{'id': 9475157,
 'description': 'An example build and deployment using GitLab continuous Integration for Singularity containers',
 'name': 'GitLab-CI',
 'name_with_namespace': 'singularityhub / GitLab-CI',
 'path': 'gitlab-ci',
 'path_with_namespace': 'singularityhub/gitlab-ci',
 'created_at': '2018-11-18T18:26:17.066Z',
 'default_branch': 'master',
 'tag_list': [],
 'ssh_url_to_repo': 'git@gitlab.com:singularityhub/gitlab-ci.git',
 'http_url_to_repo': 'https://gitlab.com/singularityhub/gitlab-ci.git',
 'web_url': 'https://gitlab.com/singularityhub/gitlab-ci',
 'readme_url': 'https://gitlab.com/singularityhub/gitlab-ci/-/blob/master/README.md',
 'avatar_url': None,
 'star_count': 7,
 'forks_count': 11,
 'last_activity_at': '2020-06-19T15:04:38.987Z',
 'namespace': {'id': 2961613,
  'name': 'singularityhub',
  'path': 'singularityhub',
  'kind': 'group',
  'full_path': 'singularityhub',
  'parent_id': None,
  'avatar_url': '/uploads/-/system/group/avatar/2961613/robot-vision.png',
  'web_url': 'https://gitlab.com/groups/singularityhub'}}
```

<a id="zenodo">
### Zenodo

The "zenodo" parser is intended to parse a Zenodo DOI or url into a software repository,
and we use the [Zenodo API](https://developers.zenodo.org/) to handle this.
 A `RSE_ZENODO_TOKEN` is required to be exported to the environment, and you can generate one under your [account application settings](https://zenodo.org/account/settings/applications/).

```bash
export RSE_ZENODO_TOKEN=123456.......
```

#### Example Usage

To use the Zenodo parser with the Research Software Encyclopedia, you can try
adding the DOI identifier. If there is a GitHub or GitLab record associated, it will
be added, and the doi for zenodo included.

```bash
$ rse add 10.5281/zenodo.3819202
INFO:rse.main:Database: filesystem
INFO:rse.main.database.filesystem:github/CLARIAH/grlc was added to the the database.
```

On the other hand, if you try to add a record that doesn't have a GitHub identifier,
you'll see this response:

```bash
$ rse add 10.5281/zenodo.1012531
INFO:rse.main:Database: filesystem
WARNING:rse.main.parsers.zenodo:Repository url not found with Zenodo record, skipping add.
```

Example usage of the parser outside of the Encyclopedia might look like the following.
If you want to instantiate an empty parser (not associated with a software repository)
you can do that as follows:

```python
from rse.main.parsers import ZenodoParser
parser = ZenodoParser()
```

However, it's more likely that you want to parse a specific repository. Let's say
that we want to parse the [Singularity Registry](https://zenodo.org/record/1012531#.Xu5OOZZME5k) 
record on Zenodo. We need to provide the DOI to do this:

```python
from rse.main.parsers import ZenodoParser

parser = ZenodoParser('10.5281/zenodo.1012531')
```

after, we can see the unique id is assigned:

```python
parser.uid
# 'zenodo/10.5281/zenodo.1012531'
```
If you provide an incorrectly formatted it, it will raise an error:

```python
parser = ZenodoParser('10.5281/zenodo.xxxxx')   
...
RuntimeError: 10.5281/zenodo.xxxxx does match a Zenodo DOI.
```

Note that you can also get a named zenodo parser, and set a unique resource identifier after the fact:

```python
from rse.main.parsers import get_named_parser 
parser = get_named_parser('zenodo')

parser.set_uid('10.5281/zenodo.1012531')
parser.uid
# 'zenodo/10.5281/zenodo.1012531'
```

Once the identifier is loaded, you can parse updated metadata for it.
Note that you can define an `RSE_ZENODO_TOKEN` to be set in the environment
if you want to potentially increase your API limits.
You can then get the metadata about the archive. Note that if the record
doesn't have a GitHub association (and you want to return the Zenodo response) you
need to set `require_repo` to False:

```python
data = parser.get_metadata(require_repo=False)

{'conceptdoi': '10.5281/zenodo.1012530',
 'conceptrecid': '1012530',
 'created': '2017-10-15T12:01:44.261541+00:00',
 'doi': '10.5281/zenodo.1012531',
 'files': [{'bucket': '66ebd044-2964-4051-8a92-c453da4709e0',
   'checksum': 'md5:d5f196461893f65b7e0294dd8386a439',
   'key': 'sregistry-1.0.1.tar.gz',
   'links': {'self': 'https://zenodo.org/api/files/66ebd044-2964-4051-8a92-c453da4709e0/sregistry-1.0.1.tar.gz'},
   'size': 7681819,
   'type': 'gz'}],
 'id': 1012531,
 'links': {'badge': 'https://zenodo.org/badge/doi/10.5281/zenodo.1012531.svg',
  'bucket': 'https://zenodo.org/api/files/66ebd044-2964-4051-8a92-c453da4709e0',
  'conceptbadge': 'https://zenodo.org/badge/doi/10.5281/zenodo.1012530.svg',
  'conceptdoi': 'https://doi.org/10.5281/zenodo.1012530',
  'doi': 'https://doi.org/10.5281/zenodo.1012531',
  'html': 'https://zenodo.org/record/1012531',
  'latest': 'https://zenodo.org/api/records/1012531',
  'latest_html': 'https://zenodo.org/record/1012531',
  'self': 'https://zenodo.org/api/records/1012531'},
 'metadata': {'access_right': 'open',
  'access_right_category': 'success',
  'contributors': [{'name': 'Arfon Smith',
    'orcid': '0000-0002-3957-2474',
    'type': 'Editor'},
   {'name': 'Pjotr Prins', 'orcid': '0000-0002-8021-9162', 'type': 'Editor'},
   {'name': 'Steffen Möller',
    'orcid': '0000-0002-7187-4683',
    'type': 'Editor'}],
  'creators': [{'affiliation': 'Stanford University',
    'name': 'Vanessa Sochat',
    'orcid': '0000-0002-4387-3819'}],
  'description': '<p>Singularity Registry is a non-centralized free and Open Source infrastructure to facilitate management and sharing of institutional or personal containers.</p>',
  'doi': '10.5281/zenodo.1012531',
  'journal': {'title': 'The Journal of Open Source Software'},
  'keywords': ['containers',
   'scientific containers',
   'HPC',
   'singularity',
   'reproducibility',
   'registry',
   'web infrastructure',
   'Docker',
   'Django',
   'nginx',
   'redis'],
  'language': 'eng',
  'license': {'id': 'BSD-3-Clause'},
  'publication_date': '2017-10-15',
  'related_identifiers': [{'identifier': '10.5281/zenodo.1012530',
    'relation': 'isVersionOf',
    'scheme': 'doi'}],
  'relations': {'version': [{'count': 1,
     'index': 0,
     'is_last': True,
     'last_child': {'pid_type': 'recid', 'pid_value': '1012531'},
     'parent': {'pid_type': 'recid', 'pid_value': '1012530'}}]},
  'resource_type': {'title': 'Software', 'type': 'software'},
  'title': 'Singularity Registry'},
 'owners': [5828],
 'revision': 5,
 'stats': {'downloads': 7.0,
  'unique_downloads': 6.0,
  'unique_views': 70.0,
  'version_downloads': 7.0,
  'version_unique_downloads': 6.0,
  'version_unique_views': 69.0,
  'version_views': 75.0,
  'version_volume': 53772733.0,
  'views': 76.0,
  'volume': 53772733.0},
 'updated': '2020-01-25T07:25:02.258480+00:00'}
```

If you set it to true, None will be returned if there is no GitHub association.
If there is, you'll get back a GitHub parser with metadata and the added DOI.

You might next want to learn about the interactive [dashboard]({{ site.baseurl }}/getting-started/dashboard/).
