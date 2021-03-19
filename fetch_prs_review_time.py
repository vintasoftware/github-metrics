import math
import statistics
import arrow

from common import extract_datetime_or_none, get_author_login
from helpers import filter_valid_prs
from request_github import fetch_prs_between


def get_reviews_from_pr(pr):
    reviews_root = pr.get("reviews")

    if not reviews_root:
        return []

    reviews = reviews_root.get("nodes", [])
    if not reviews:
        return []

    return reviews


def get_first_review(pr):
    pr_author_login = get_author_login(pr)
    reviews = get_reviews_from_pr(pr)

    different_author_reviews = [
        r for r in reviews if pr_author_login != get_author_login(r)
    ]

    if not different_author_reviews:
        return

    return different_author_reviews[0]


def hours_without_review(pr):
    open_date = extract_datetime_or_none(pr.get("createdAt"))
    merge_date = extract_datetime_or_none(pr.get("mergedAt"))
    close_date = extract_datetime_or_none(pr.get("closedAt"))

    first_review = get_first_review(pr)

    first_review_date = arrow.now().shift(days=1000)
    if first_review:
        first_review_date = extract_datetime_or_none(
            arrow.get(first_review["createdAt"])
        )

    first_review_or_merge_date = min(
        [merge_date, close_date, first_review_date])

    review_timedelta = first_review_or_merge_date - open_date

    if review_timedelta.days > 500:
        return None

    return review_timedelta.total_seconds() / 3600


def hours_without_merge(pr):
    open_date = extract_datetime_or_none(pr.get("createdAt"))
    merge_date = extract_datetime_or_none(pr.get("mergedAt"))
    import ipdb
    ipdb.set_trace()
    review_timedelta = merge_date - open_date

    if review_timedelta.days > 500:
        return None

    return review_timedelta.total_seconds() / 3600


def format_prs_with_hours(prs_list, use_time_before_review=False):
    calulate_hours = (
        hours_without_review if use_time_before_review else hours_without_merge
    )
    prs_list_with_hours = [
        {
            "title": pr["title"],
            "author": get_author_login(pr),
            "reviewer": get_author_login(get_first_review(pr))
            if get_first_review(pr)
            else None,
            "hours_without_review": calulate_hours(pr),
            "created_at": extract_datetime_or_none(pr.get("createdAt")),
        }
        for pr in prs_list
    ]

    return prs_list_with_hours


def filter_prs_with_more_than_18h_before_review(prs_list, use_time_before_review=False):
    calulate_hours = (
        hours_without_review if use_time_before_review else hours_without_merge
    )
    return [pr for pr in prs_list if calulate_hours(pr) > 18]


def calulate_prs_review_time_statistics(
    start_date, end_date, include_hotfixes=False, use_time_before_review=False
):
    prs_list = fetch_prs_between(start_date, end_date)
    valid_prs_list = filter_valid_prs(
        prs_list, include_hotfixes=include_hotfixes)
    prs_more_than_18h_without_review = filter_prs_with_more_than_18h_before_review(
        valid_prs_list
    )
    valid_prs_list_with_hours = format_prs_with_hours(valid_prs_list)

    hours = sorted([pr["hours_without_review"]
                   for pr in valid_prs_list_with_hours])
    percentile_95_idx = math.floor(0.95 * len(hours))

    print(f"Median: {statistics.median(hours)} hours")
    print(f"Mean: {statistics.mean(hours)} hours")
    print(f"95 percentile: {hours[percentile_95_idx]} hours")
    print(
        f"Percent of PRs with more than 18h waiting for review: "
        f"{100 * len(prs_more_than_18h_without_review) / len(hours)}%"
    )


calulate_prs_review_time_statistics(
    start_date=arrow.get("2019-10-01"),
    end_date=arrow.get("2019-10-31T23:59:59"),
    include_hotfixes=False,
)
