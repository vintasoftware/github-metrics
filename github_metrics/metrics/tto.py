import numpy

from github_metrics.common import extract_datetime_or_none, get_author_login
from github_metrics.helpers import filter_valid_prs, format_timedelta, get_time_without_weekend
from github_metrics.request_github import fetch_prs_between


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


def call_time_to_open_statistics(
    start_date, end_date, include_hotfixes=False, exclude_authors=[], exclude_weekends=False
):
    prs_list = fetch_prs_between(start_date, end_date)
    valid_prs_list = filter_valid_prs(
        prs_list, include_hotfixes=include_hotfixes, exclude_authors=exclude_authors
    )
    formatted_prs_list = format_prs_list(valid_prs_list)

    if not formatted_prs_list or formatted_prs_list == []:
        return "There are no valid PRs to pull this data from, please select another timeframe"

    time_to_open = []
    for pr in formatted_prs_list:
        first_commit_time = pr["commits"][0]["commited_at"]
        timedelta = pr["created_at"] - first_commit_time
        if exclude_weekends:
            timedelta = get_time_without_weekend(first_commit_time, pr["created_at"])
        time_to_open.append(timedelta)

    mean = numpy.mean(time_to_open)
    median = numpy.median(time_to_open)
    percentile = numpy.percentile(time_to_open, 95)

    print(
        f"""
            \033[1mTime to open\033[0m
            ----------------------------------
            Total PRs calculated: {len(formatted_prs_list)}
            ----------------------------------
            Mean: {format_timedelta(mean)} ({round(mean.total_seconds()/3600, 2)} hours)
            Median: {format_timedelta(median)} ({round(median.total_seconds()/3600, 2)} hours)
            95 percentile: {format_timedelta(percentile)} ({round(percentile.total_seconds()/3600, 2)} hours)
            """
    )
