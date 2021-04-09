# github-metrics

## About

A script for getting your team PRs metrics.

## Running

The run command takes 3 arguments. In order they are:

`metric`: The abbreviation of the metric you'd like to calculate

`start date`: The metric start date. Date in format YYYY-mm-dd

`end date`: The metric cutoff date. Be aware that this date will not included in the range calculation. Date in format YYYY-mm-dd

#### Time To Merge
`python run.py ttm 2021-03-22 2021-03-24`

#### Time to Review
`python run.py ttr 2020-11-10 2020-11-18`

## Metrics available
### Time To Merge (ttm)
The Time to Merge metric calculates time between the first commit of a given branch, and the merge action of it's pull request.

### Time To Review (ttr)
It calculates the time a PR waited for, or has been waiting for the first review since the PR opened.

## Project setup

### Dependencies setup
1. Create a virtual enviroment `virtualenv venv`
2. Install dependencies with `pip install -r requirements.txt`

### Project variables setup
1. Create a .env file by copying from .env.example with `cp .env.example .env`
2.  Fill settings variables:

`REPOSITORY_NAME`: The repository name of the project of your choice 

`ORG_NAME`: The name of the organization where the repository is located

`GITHUB_LOGIN`: Your github account login

`GITHUB_TOKEN`: An access token generated with your github account.  More information accessible through [this guide](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)
