import math
import statistics
from time import sleep

import arrow
import requests
from requests.auth import HTTPBasicAuth
from settings import GITHUB_LOGIN, GITHUB_TOKEN, REPOSITORY_NAME, ORG_NAME


def extract_datetime_or_none(isoformat_str_date):
    if not isoformat_str_date:
        return arrow.now().shift(days=1000)

    try:
        arrow_date = arrow.get(isoformat_str_date)
    except Exception:
        return arrow.now().shift(days=1000)

    return arrow_date.datetime


def format_request_for_github(cursor=None):
    after = ""
    if cursor:
        after = f', after: "{cursor}"'

    return """{{
    organization(login: "{ORG_NAME}") {{
        repository(name: "{REPOSITORY_NAME}") {{
            pullRequests(
                first: 100,
                orderBy: {{
                    field: CREATED_AT,
                    direction: DESC
                }}{after}
            ) {{
                pageInfo {{
                    endCursor
                    startCursor
                    hasNextPage
                }}
                nodes {{
                    id
                    title
                    createdAt
                    baseRefName
                    headRefName
                    reviews(first: 10) {{
                        nodes {{
                            createdAt
                            state
                            author {{
                                login
                            }}
                        }}
                    }}
                    author {{
                        login
                    }}
                    mergedAt
                    closedAt
                    commits(first: 10) {{
                        edges {{
                            node {{
                                commit {{
                                    oid
                                    message
                                    committedDate
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}
}}""".format(
        after=after, ORG_NAME=ORG_NAME, REPOSITORY_NAME=REPOSITORY_NAME
    )


def pr_was_created_between(pr, start_date, end_date):
    open_date = extract_datetime_or_none(pr.get("createdAt"))

    return open_date >= start_date and open_date <= end_date


def fetch_prs_between(start_date, end_date):
    prs_list = []
    current_date = None
    cursor = None
    has_next_page = True
    while has_next_page and (not current_date or current_date > start_date):
        response = requests.post(
            "https://api.github.com/graphql",
            auth=HTTPBasicAuth(GITHUB_LOGIN, GITHUB_TOKEN),
            json={"query": format_request_for_github(cursor)},
        )
        data = response.json().get("data")

        if not data:
            has_next_page = False
            continue

        organization = data.get("organization")
        if not organization:
            has_next_page = False
            continue

        repository = organization.get("repository")
        if not repository:
            has_next_page = False
            continue

        prs = repository.get("pullRequests")
        if not prs:
            has_next_page = False
            continue

        page_info = prs.get("pageInfo")
        if not page_info:
            has_next_page = False
            continue

        has_next_page = page_info["hasNextPage"]
        cursor = page_info["endCursor"]

        page_prs_list = prs.get("nodes")
        if not page_prs_list:
            has_next_page = False
            continue

        current_date = extract_datetime_or_none(page_prs_list[-1]["createdAt"])

        prs_list += [
            pr
            for pr in page_prs_list
            if pr_was_created_between(pr, start_date, end_date)
        ]
        # request debug logs
        # print(f"Has next page: {has_next_page}")
        # print(f"Current date: {current_date.isoformat()}")
        # print(f"current_date > start_date: {current_date > start_date}")
        sleep(1)

    return prs_list


def is_closed(pr):
    return pr.get("closedAt") is not None and not pr.get("mergedAt")


def is_release(pr):
    release_in_head_branch_name = "release" in pr["headRefName"].lower()
    release_in_title = "release" in pr["title"].lower()
    head_branch_is_master = "master" in pr["headRefName"].lower()
    base_branch_is_production = "production" in pr["baseRefName"].lower()

    if not base_branch_is_production:
        return False

    return release_in_head_branch_name or head_branch_is_master or release_in_title


def is_hotfix(pr):
    hotfix_in_head_branch_name = "hotfix" in pr["headRefName"].lower()
    hotfix_in_title = "hotfix" in pr["title"].lower()
    base_branch_is_production = "production" in pr["baseRefName"].lower()

    if not base_branch_is_production:
        return False

    return hotfix_in_head_branch_name or hotfix_in_title


def is_merge_back_from_prod(pr):
    base_branch_is_master = "master" in pr["baseRefName"].lower()
    head_branch_is_production = "production" in pr["headRefName"].lower()

    return base_branch_is_master or head_branch_is_production


def exclude_closeds(prs_list):
    return [pr for pr in prs_list if not is_closed(pr)]


def exclude_releases(prs_list):
    return [pr for pr in prs_list if not is_release(pr)]


def exclude_hotfixes(prs_list):
    return [pr for pr in prs_list if not is_hotfix(pr)]


def exclude_merge_backs_from_prod(prs_list):
    return [pr for pr in prs_list if not is_merge_back_from_prod(pr)]


def get_author_login(pr_or_review):
    author = pr_or_review.get("author")
    if not author:
        return

    return author.get("login")


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

    first_review_or_merge_date = min([merge_date, close_date, first_review_date])

    review_timedelta = first_review_or_merge_date - open_date

    if review_timedelta.days > 500:
        return None

    return review_timedelta.total_seconds() / 3600


def hours_without_merge(pr):
    open_date = extract_datetime_or_none(pr.get("createdAt"))
    merge_date = extract_datetime_or_none(pr.get("mergedAt"))

    review_timedelta = merge_date - open_date

    if review_timedelta.days > 500:
        return None

    return review_timedelta.total_seconds() / 3600


def filter_valid_prs(prs_list, include_hotfixes=True):
    valid_prs_list = exclude_merge_backs_from_prod(
        exclude_releases(exclude_closeds(prs_list))
    )

    if not include_hotfixes:
        valid_prs_list = exclude_hotfixes(valid_prs_list)

    return valid_prs_list


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
    valid_prs_list = filter_valid_prs(prs_list, include_hotfixes=include_hotfixes)
    prs_more_than_18h_without_review = filter_prs_with_more_than_18h_before_review(
        valid_prs_list
    )
    valid_prs_list_with_hours = format_prs_with_hours(valid_prs_list)

    hours = sorted([pr["hours_without_review"] for pr in valid_prs_list_with_hours])
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
