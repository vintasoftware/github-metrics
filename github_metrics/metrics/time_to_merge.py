import numpy

from github_metrics.common import extract_datetime_or_none, get_author_login
from github_metrics.helpers import (
    filter_valid_prs,
    format_timedelta_to_hours,
    format_timedelta_to_text,
    get_time_without_weekend,
)


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


def format_pr_list(pr_list):
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
        for pr in pr_list
    ]


def get_merged_prs(formatted_pr_list):
    merged_prs = []

    for pr in formatted_pr_list:
        if pr["merged_at"] is not None:
            merged_prs.append(pr)
    return merged_prs


def get_time_to_merge_data(
    pr_list,
    include_hotfixes,
    exclude_authors,
    filter_authors,
    exclude_weekends,
):
    valid_pr_list = filter_valid_prs(
        pr_list, include_hotfixes, exclude_authors, filter_authors
    )
    formatted_pr_list = format_pr_list(valid_pr_list)
    merged_prs = get_merged_prs(formatted_pr_list)

    if not merged_prs or merged_prs == []:
        return "There are no valid PRs to pull this data from, please select another timeframe"

    time_to_merge_list = []
    for pr in merged_prs:
        first_commit_time = pr["commits"][0]["commited_at"]
        timedelta = pr["merged_at"] - first_commit_time
        if exclude_weekends:
            timedelta = get_time_without_weekend(first_commit_time, pr["merged_at"])
        time_to_merge_list.append(timedelta)

    mean = numpy.mean(time_to_merge_list)
    median = numpy.median(time_to_merge_list)
    percentile = numpy.percentile(time_to_merge_list, 95)
    return {
        "mean": mean,
        "median": median,
        "percentile_95": percentile,
        "mean_duration_in_hours": mean.total_seconds() / 3600,
        "median_duration_in_hours": median.total_seconds() / 3600,
        "percentile_95_duration_in_hours": percentile.total_seconds() / 3600,
        "merged_prs": merged_prs,
    }


def call_mean_time_to_merge_statistics(
    pr_list,
    include_hotfixes,
    exclude_authors,
    filter_authors,
    exclude_weekends,
):
    data = get_time_to_merge_data(
        pr_list=pr_list,
        include_hotfixes=include_hotfixes,
        exclude_authors=exclude_authors,
        filter_authors=filter_authors,
        exclude_weekends=exclude_weekends,
    )

    print(
        f"     \033[1mTime to merge\033[0m\n"
        f"     ----------------------------------\n"
        f"     Total PRs calculated: {len(data['merged_prs'])}\n"
        f"     ----------------------------------\n"
        f"     Mean: {format_timedelta_to_text(data['mean'])}"
        f" ({format_timedelta_to_hours(data['mean'])} hours)\n"
        f"     Median: {format_timedelta_to_text(data['median'])}"
        f" ({format_timedelta_to_hours(data['median'])} hours)\n"
        f"     95 percentile: {format_timedelta_to_text(data['percentile_95'])}"
        f" ({format_timedelta_to_hours(data['percentile_95'])} hours)\n"
    )
