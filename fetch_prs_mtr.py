import arrow
import numpy

from common import extract_datetime_or_none, get_author_login
from helpers import filter_valid_prs, format_timedelta
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
    open_date = extract_datetime_or_none(pr["created_at"])

    if pr["first_review_at"] is None:
        time_without_review = arrow.now() - open_date
        return time_without_review.total_seconds() / 3600

    time_without_review = extract_datetime_or_none(pr["first_review_at"]) - open_date
    return time_without_review.total_seconds() / 3600


def filter_prs_with_more_than_18h_before_review(prs_list, use_time_before_review=False):
    return [pr for pr in prs_list if hours_without_review(pr) > 18]


def format_prs_list(prs_list):
    prs_list_with_hours = [
        {
            "title": pr["title"],
            "author": get_author_login(pr),
            "first_review_at": extract_datetime_or_none(
                get_first_review(pr).get("createdAt")
            )
            if get_first_review(pr)
            else None,
            "created_at": extract_datetime_or_none(pr.get("createdAt")),
        }
        for pr in prs_list
    ]

    return prs_list_with_hours


def filter_reviewed_prs(prs_list):
    return [pr for pr in prs_list if pr["first_review_at"] is not None]


def calulate_prs_review_time_statistics(start_date, end_date, include_hotfixes=False):
    prs_list = fetch_prs_between(start_date, end_date)
    valid_prs_list = filter_valid_prs(prs_list, include_hotfixes=include_hotfixes)
    formatted_prs_list = format_prs_list(valid_prs_list)
    reviewed_prs = filter_reviewed_prs(formatted_prs_list)
    prs_more_than_18h_without_review = filter_prs_with_more_than_18h_before_review(
        formatted_prs_list
    )

    review_time_list = []
    for pr in reviewed_prs:
        review_time = pr["first_review_at"] - pr["created_at"]
        review_time_list.append(review_time)

    print(
        f"""
            \033[1mMean time to review\033[0m
            ----------------------------------
            Total valid PRs: {len(formatted_prs_list)}
            PRs without review: {len(formatted_prs_list) - len(reviewed_prs)} ({(len(formatted_prs_list) - len(reviewed_prs)) * 100 / len(formatted_prs_list)}%)
            PRs with more than 18h without review: {len(prs_more_than_18h_without_review)} ({len(prs_more_than_18h_without_review) * 100 / len(formatted_prs_list)}%)
            ----------------------------------
            Mean: {format_timedelta(numpy.mean(review_time_list))}
            Median: {format_timedelta(numpy.median(review_time_list))}
            95 percentile: {format_timedelta(numpy.percentile(review_time_list, 95))}
        """
    )