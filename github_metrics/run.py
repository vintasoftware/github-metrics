import os

import arrow
import click

from github_metrics.metrics.all import call_all_metrics
from github_metrics.metrics.hotfixes_count import count_hotfixes
from github_metrics.metrics.prs_count import count_prs
from github_metrics.metrics.merge_rate import call_merge_rate_statistics
from github_metrics.metrics.open_to_merge import (
    calulate_prs_open_to_merge_time_statistics,
)
from github_metrics.metrics.pr_size import call_pr_size_statistics
from github_metrics.metrics.time_to_merge import call_mean_time_to_merge_statistics
from github_metrics.metrics.time_to_open import call_time_to_open_statistics
from github_metrics.metrics.time_to_review import calulate_prs_review_time_statistics
from github_metrics.request import fetch_prs_between
from github_metrics.settings import BASE_DIR


def setup_enviroment_variables():
    github_username = input("Github username: ")
    github_token = input("Github token: ")
    organization_name = input("Name of the organization: ")
    repository_name = input("Repository name: ")

    with open(os.path.join(BASE_DIR, ".env"), "w") as file:
        content = "\n".join(
            [
                f"GITHUB_LOGIN={github_username}",
                f"GITHUB_TOKEN={github_token}",
                f"ORG_NAME={organization_name}",
                f"REPOSITORY_NAME={repository_name}",
            ]
        )
        file.write(content)


@click.command()
@click.option(
    "--setup",
    is_flag=True,
    default=False,
    help="Setup your enviroment variables",
)
@click.option(
    "--metric",
    type=str,
    help="""The reference of the metric you'd like to run:

    \b
    ttm - Time to Merge
    ttr - Time to Review
    tto - Time to Open
    otm - Open To Merge Time
    mr - Merge Rate
    pr_size - Pull Request Size
    hotfixes_count - Hotfixes Count
    prs_count - Pull Requests Count
    \b""",
)
@click.option(
    "--start-date",
    type=str,
    help="""The metric start date.

    Date in format YYYY-mm-dd""",
)
@click.option(
    "--end-date",
    type=str,
    help="""The metric cutoff date.

    Date in format YYYY-mm-dd""",
)
@click.option(
    "--include-hotfixes",
    is_flag=True,
    default=False,
    help="Will include all hotfixes in the metric calculation.",
)
@click.option(
    "--exclude-authors",
    type=str,
    help="""
        List of PR authors separated by a comma to be removed from metric.

        eg.: username,other_username""",
)
@click.option(
    "--filter-authors",
    type=str,
    help="""
        Will calculate prs created only by the authors listed in here.

        eg.: username,other_username""",
)
@click.option(
    "--exclude-weekends",
    is_flag=True,
    default=False,
    help="Will exclude weekends from time metric.",
)
def cli(
    metric,
    start_date,
    end_date,
    include_hotfixes,
    exclude_authors,
    filter_authors,
    exclude_weekends,
    setup,
):
    """
    Generates metrics from Github API.
    """

    if setup:
        setup_enviroment_variables()
        return

    start_date = arrow.get(start_date)
    end_date = arrow.get(f"{end_date}T23:59:59")

    exclude_user_list = []
    if exclude_authors:
        exclude_user_list = exclude_authors.split(",")

    filter_user_list = []
    if filter_authors:
        filter_user_list = filter_authors.split(",")

    pr_list = fetch_prs_between(start_date, end_date)
    if metric == "ttm":
        call_mean_time_to_merge_statistics(
            pr_list,
            include_hotfixes,
            exclude_user_list,
            filter_user_list,
            exclude_weekends,
        )
    elif metric == "ttr":
        calulate_prs_review_time_statistics(
            pr_list,
            include_hotfixes,
            exclude_user_list,
            filter_user_list,
            exclude_weekends,
        )
    elif metric == "tto":
        call_time_to_open_statistics(
            pr_list,
            include_hotfixes,
            exclude_user_list,
            filter_user_list,
            exclude_weekends,
        )
    elif metric == "otm":
        calulate_prs_open_to_merge_time_statistics(
            pr_list,
            include_hotfixes,
            exclude_user_list,
            filter_user_list,
            exclude_weekends,
        )
    elif metric == "mr":
        call_merge_rate_statistics(
            pr_list, include_hotfixes, exclude_user_list, filter_user_list
        )
    elif metric == "pr_size":
        call_pr_size_statistics(
            pr_list, include_hotfixes, exclude_user_list, filter_user_list
        )
    elif metric == "prs_count":
        count_prs(pr_list, include_hotfixes, exclude_user_list, filter_user_list)
    else:
        call_all_metrics(
            pr_list,
            include_hotfixes,
            exclude_user_list,
            filter_user_list,
            exclude_weekends,
        )
