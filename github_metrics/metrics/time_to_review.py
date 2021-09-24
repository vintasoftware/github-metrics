import arrow
import numpy

from github_metrics.common import extract_datetime_or_none, get_author_login
from github_metrics.helpers import (
    filter_valid_prs,
    format_timedelta_to_hours,
    format_timedelta_to_text,
    get_time_without_weekend,
)


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


def filter_prs_with_more_than_24h_before_review(pr_list, use_time_before_review=False):
    return [pr for pr in pr_list if hours_without_review(pr) > 24]


def format_pr_list(pr_list):
    pr_list_with_hours = [
        {
            "title": pr["title"],
            "author": get_author_login(pr),
            "created_at": extract_datetime_or_none(pr.get("createdAt")),
            "first_review_at": extract_datetime_or_none(
                get_first_review(pr).get("createdAt")
            )
            if get_first_review(pr)
            else None,
        }
        for pr in pr_list
    ]

    return pr_list_with_hours


def filter_reviewed_prs(pr_list):
    return [pr for pr in pr_list if pr["first_review_at"] is not None]


def get_time_to_review_data(
    pr_list, include_hotfixes, exclude_authors, filter_authors, exclude_weekends
):
    valid_pr_list = filter_valid_prs(
        pr_list, include_hotfixes, exclude_authors, filter_authors
    )
    formatted_pr_list = format_pr_list(valid_pr_list)
    reviewed_prs = filter_reviewed_prs(formatted_pr_list)
    prs_more_than_24h_without_review = filter_prs_with_more_than_24h_before_review(
        formatted_pr_list
    )

    review_time_list = []
    for pr in reviewed_prs:
        review_time = pr["first_review_at"] - pr["created_at"]
        if exclude_weekends:
            review_time = get_time_without_weekend(
                pr["created_at"], pr["first_review_at"]
            )
        review_time_list.append(review_time)

    total_prs = len(formatted_pr_list)
    unreviewed_prs = total_prs - len(reviewed_prs)
    prs_over_24h = len(prs_more_than_24h_without_review)

    mean = numpy.mean(review_time_list)
    median = numpy.median(review_time_list)
    percentile = numpy.percentile(review_time_list, 95)
    return {
        "mean": mean,
        "median": median,
        "percentile_95": percentile,
        "total_prs": formatted_pr_list,
        "unreviewed_prs": unreviewed_prs,
        "prs_over_24h": prs_over_24h,
    }


def calulate_prs_review_time_statistics(
    pr_list, include_hotfixes, exclude_authors, filter_authors, exclude_weekends
):
    data = get_time_to_review_data(
        pr_list, include_hotfixes, exclude_authors, filter_authors, exclude_weekends
    )

    print(
        f"     \033[1mTime to review\033[0m\n"
        f"    ----------------------------------\n"
        f"    Total valid PRs: {len(data['total_prs'])}\n"
        f"    Unreviewed PRs: {data['unreviewed_prs']}"
        f" ({round((data['unreviewed_prs'] * 100) / len(data['total_prs']), 2)}%)\n"
        f"    PRs with more than 24h waiting for review: {data['prs_over_24h']}"
        f" ({round(data['prs_over_24h'] * 100 / len(data['total_prs']), 2)}%)\n"
        f"    ----------------------------------\n"
        f"    Mean: {format_timedelta_to_text(data['mean'])}"
        f" ({format_timedelta_to_hours(data['mean'])} hours)\n"
        f"    Median: {format_timedelta_to_text(data['median'])}"
        f" ({format_timedelta_to_hours(data['median'])} hours)\n"
        f"    95 percentile: {format_timedelta_to_text(data['percentile_95'])}"
        f" ({format_timedelta_to_hours(data['percentile_95'])} hours)\n"
    )
