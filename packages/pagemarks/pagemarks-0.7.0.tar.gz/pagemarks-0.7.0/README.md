# pagemarks

Free, git-backed, self-hosted bookmarks

## Requirements

- Git (1.7.x or newer)
- Python >= 3.10

### Status

Under development - do not use yet


## Bookmark File Format

Each bookmark is stored in a JSON document with the following fields:

| Field        | Type             | Mandatory? | Description                         |
|:-------------|:-----------------|:----------:|:------------------------------------|
| `name`       | string           | no         | the bookmark's title                |
| `url`        | string           | YES        | the bookmark's URL                  |
| `tags`       | array of strings | no         | Tags must be `[a-z0-9_-]{1,20}`, that is 20 characters or shorter, lower-case alphanumeric plus hyphen and underscore. |
| `notes`      | string           | no         | plain text notes about the bookmark |
| `date_added` | string           | no         | Date when the bookmark was added, in the format `2021-08-05 16:12:00`. A date-only format is possible (`2018-10-15`) in which case the time is assumed to be `00:00:00`. The timezone is always UTC. Missing dates are treated as the epoch. |


## Development

Refresh CI image:

    docker login registry.gitlab.com
    docker pull python:3.10-slim-bullseye
    docker build -t registry.gitlab.com/barfuin/pagemarks/ci:latest -f Dockerfile.ci --progress=plain .
    docker push registry.gitlab.com/barfuin/pagemarks/ci:latest
