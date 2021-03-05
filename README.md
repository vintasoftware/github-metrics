# github-metrics

## About

A script for getting your team PRs metrics.

This project was conceived to be part of the 2021 VBP.

### Metrics available
Coming soon

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