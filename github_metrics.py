import click
import arrow

from ttm import call_mean_time_to_merge_statistics
from ttr import calulate_prs_review_time_statistics
from mr import call_merge_rate_statistics
from pr_size import call_pr_size_statistics


@click.command()
@click.option(
    "--metric",
    type=str,
    required=True,
    help="The reference of the metric you'd like to run",
)
@click.option(
    "--start-date",
    type=str,
    required=True,
    help="The metric start date. Date in format YYYY-mm-dd",
)
@click.option(
    "--end-date",
    type=str,
    required=True,
    help="The metric cutoff date. Date in format YYYY-mm-dd",
)
@click.option(
    "--include-hotfixes",
    type=bool,
    default=False,
    help="Will include all hotfixes in the metric calculation.",
)
@click.option(
    "--exclude-authors",
    type=str,
    help="List of PR authors separated by a comma to be removed from metric",
)
def cli(metric, start_date, end_date, include_hotfixes, exclude_authors):
    """
    Generates metrics from Github API.
    """
    start_date = arrow.get(start_date)
    end_date = arrow.get(f"{end_date}T23:59:59")

    user_list = []
    if exclude_authors:
        user_list = exclude_authors.split(",")

    if metric == "ttm":
        call_mean_time_to_merge_statistics(
            start_date, end_date, include_hotfixes, user_list
        )
    elif metric == "ttr":
        calulate_prs_review_time_statistics(
            start_date, end_date, include_hotfixes, user_list
        )
    elif metric == "mr":
        call_merge_rate_statistics(start_date, end_date, include_hotfixes, user_list)
    elif metric == "pr_size":
        call_pr_size_statistics(start_date, end_date, include_hotfixes, user_list)
