import math
import statistics
import arrow
import numpy

from common import extract_datetime_or_none, get_author_login
from helpers import filter_valid_prs, format_timedelta
from request_github import fetch_prs_between


def get_formatted_list_of_commits(commit_data):
    commits_list = []

    if not commit_data.get("edges"):
        return []

    for data in commit_data.get("edges"):
        commit = data.get("node").get("commit")
        commits_list.append(
            {
                "message": commit.get("message"),
                "commited_at": extract_datetime_or_none(commit.get("committedDate")),
            }
        )
    return commits_list


def format_prs_list(prs_list, use_time_before_review=False):
    prs_list_with_hours = [
        {
            "title": pr["title"],
            "author": get_author_login(pr),
            "created_at": extract_datetime_or_none(pr.get("createdAt")),
            "merged_at": extract_datetime_or_none(pr.get("mergedAt")),
            "closed_at": extract_datetime_or_none(pr.get("closedAt")),
            "commits": get_formatted_list_of_commits(pr.get("commits")),
        }
        for pr in prs_list
    ]

    return prs_list_with_hours


def call_mean_time_to_merge_statistics(
    start_date, end_date, include_hotfixes=False, use_time_before_review=False
):
    prs_list = fetch_prs_between(start_date, end_date)
    valid_prs_list = filter_valid_prs(
        prs_list, include_hotfixes=include_hotfixes)

    formatted_prs_list = format_prs_list(valid_prs_list)

    time_to_merge_list = []
    for pr in formatted_prs_list:
        first_commit_time = pr.get("commits")[0].get("commited_at")
        merged_timedelta = pr.get("merged_at") - first_commit_time
        time_to_merge_list.append(merged_timedelta)

    print(f"Mean: {format_timedelta(numpy.mean(time_to_merge_list))} hours")
    print(f"Median: {format_timedelta(numpy.median(time_to_merge_list))}")
    print(
        f"95 percentile: {format_timedelta(numpy.percentile(time_to_merge_list, 95))} hours")


call_mean_time_to_merge_statistics(
    start_date=arrow.get("2019-10-01"),
    end_date=arrow.get("2019-10-31T23:59:59"),
    include_hotfixes=False,
)
