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


def format_prs_list(prs_list):
    return [
        {
            "title": pr["title"],
            "author": get_author_login(pr),
            "created_at": extract_datetime_or_none(pr.get("createdAt")),
            "merged_at": extract_datetime_or_none(pr.get("mergedAt"))
            if pr.get("mergedAt")
            else None,
            "closed_at": extract_datetime_or_none(pr.get("closedAt"))
            if pr.get("closedAt")
            else None,
            "commits": get_formatted_list_of_commits(pr.get("commits")),
        }
        for pr in prs_list
    ]


def get_merged_prs(formatted_prs_list):
    merged_prs = []

    for pr in formatted_prs_list:
        if pr["merged_at"] is not None:
            merged_prs.append(pr)
    return merged_prs


def call_mean_time_to_merge_statistics(start_date, end_date, include_hotfixes=False):
    prs_list = fetch_prs_between(start_date, end_date)

    valid_prs_list = filter_valid_prs(prs_list, include_hotfixes=include_hotfixes)

    formatted_prs_list = format_prs_list(valid_prs_list)
    merged_prs = get_merged_prs(formatted_prs_list)

    if not merged_prs:
        return "There are no valid PRs to pull this data from, please select another timeframe"

    time_to_merge_list = []
    for pr in merged_prs:
        first_commit_time = pr["commits"][0]["commited_at"]
        merged_timedelta = pr["merged_at"] - first_commit_time
        time_to_merge_list.append(merged_timedelta)

    return f"""
            Total PRs calculated: {len(merged_prs)}\n
            Mean: {format_timedelta(numpy.mean(time_to_merge_list))}\n
            Median: {format_timedelta(numpy.median(time_to_merge_list))}\n
            95 percentile: {format_timedelta(numpy.percentile(time_to_merge_list, 95))}
            """
