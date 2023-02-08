# github-metrics

## About

A script for getting your team PRs metrics.

## Running

The run command takes the following arguments:

`--metric`: The reference for the metric you'd like to calculate. If no metric is provided, it will calculate all metrics available.

`--start-date`: The metric start date. Date in format YYYY-mm-dd

`--end-date`: The metric cutoff date. Date in format YYYY-mm-dd

`--exclude-authors`: Will exclude all PRs created by the listed authors. This argument must list usernames separated by a comma. Example: `--exclude_authors=pantoja,github_username,other_username`

`--filter-authors`: Will take into consideration only the PRs created by the authors in this list. This argument must list usernames separated by a comma. Example: `--exclude_authors=pantoja,github_username,other_username`

`--include-hotfixes`: Will include all hotfixes in the metric calculation. By default, this value is false.

`--exclude-weekends`: Will exclude weekend time from time metrics (time to merge, time to open, time to review).

#### [All]
`github_metrics --start-date=2021-03-22 --end-date=2021-03-24`

#### [Time To Merge](#ttm)
`github_metrics --metric=ttm --start-date=2021-03-22 --end-date=2021-03-24`

#### [Time to Review](#ttr)
`github_metrics --metric=ttr --start-date=2020-11-10 --end-date=2020-11-18`

#### [Time to Open](#tto)
`github_metrics --metric=tto --start-date=2020-11-10 --end-date=2020-11-18`

#### [Open to Merge Time](#otm)
`github_metrics --metric=otm --start-date=2020-11-10 --end-date=2020-11-18`

#### [Merge Rate](#mr)
`github_metrics --metric=mr --start-date=2021-03-22 --end-date=2021-03-24`

#### [Pull Request Size](#pr-size)
`github_metrics --metric=pr_size --start-date=2020-11-10 --end-date=2020-11-18`

#### [Hotfixes count](#hotfixes-count)
`github_metrics --metric=hotfixes_count --start-date=2020-11-10 --end-date=2020-11-18`

## Metrics available
- <b id="ttm">Time To Merge (ttm):</b>
The Time to Merge metric calculates time between the first commit of a given branch, and the merge action of it's pull request.

- <b id="ttr">Time To Review (ttr):</b>
It calculates the time a PR waited for, or has been waiting for the first review since the PR opened.

- <b id="tto">Time To Open (tto):</b>
The time elapsed between a user's first commit to a branch and opening a pull request for that branch.

- <b id="tto">Open To Merge Time (otm):</b>
Returns statistics related to the time between opening and merging a pull request.

- <b id="mr">Merge Rate (mr):</b>
It measures the total number of merged pull requests to the total number of developers active in this time period (number of merged PRS / dev). A value closer to 1 indicates that each developer is merging a PR. a higher number indicates more merged PRs than devs, and vice versa.

- <b id="pr-size">Pull Request Size (pr_size):</b>
It generates metrics related to the number of lines added and deleted in a PR. The output will generate metrics related to the sum of different lines in a pr (lines added + lines deleted), and the addition rate metric (lines added / lines deleted). In the latter case, a higher the rate number means more lines are being added than deleted.

- <b id="hotfixes-count">Hotfixes Count (hotfixes_count):</b>
The number of hotfixes in the period.

## Installing the project
1. Install using `pip install github-metrics`
2. Setup settings variable by running `github_metrics --setup`. You'll be asked to give following information:

`Github username`: Your github account login

`Enter a github token`: An access token generated with your github account. More information accessible through [this guide](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token). The lib requires full repo access for it to work

`Name of the organization`: The name of the organization where the repository is located

`Repository name`: The repository name of the project of your choice

**NOTE:** Running the `--setup` flag will overwrite the existing environment settings.

## Project setup

### Dependencies setup
1. Create a virtual enviroment `virtualenv venv`
2. Install dependencies with `pip install --editable .`

### Setup with docker
1. Run the command with `docker-compose run app {}`. e.g. `docker-compose run app github_metrics --metric=ttm --start-date=2021-03-22 --end-date=2021-03-24`

### Project variables setup
1. Create a .env file by copying from .env.example with `cp .env.example .env`
2.  Fill settings variables:

`REPOSITORY_NAME`: The name of the repository
`ORG_NAME`: The name of the organization
`GITHUB_LOGIN`: Your github account username
`GITHUB_TOKEN`: The access token generated with your github account.

![image](https://user-images.githubusercontent.com/38823219/117503308-27d1ab80-af57-11eb-845c-a8640cfe023d.png)


Release Process
===============

For maintainers only:

- Run `rm -rf build dist` to delete current build archives
- Install dependencies with `pip install -r ./requirements.txt`. Make sure you are inside a virtual environment
- Run ``bump2version <minor|major|patch>`` to update the version number (pick one of the options)

    - Version number on ``github_metrics/__init__.py`` and ``setup.py`` will be updated automatically
    - You can specify the ``--new_version`` flag in case you wish to manually set the newest version (if not provided, it will be done automatically based on the chosen option)
- Build the artifacts with `python setup.py sdist bdist_wheel --universal`
- Upload the new version with `twine upload dist/*`
