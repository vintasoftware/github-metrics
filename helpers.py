from common import get_author_login
import datetime


def is_closed(pr):
    return pr.get("closedAt") is not None and not pr.get("mergedAt")


def is_release(pr):
    release_in_head_branch_name = "release" in pr["headRefName"].lower()
    release_in_title = "release" in pr["title"].lower()
    head_branch_is_master = (
        "master" in pr["headRefName"].lower() or "main" in pr["headRefName"].lower()
    )
    base_branch_is_production = "production" in pr["baseRefName"].lower()

    if not base_branch_is_production:
        return False

    return release_in_head_branch_name or head_branch_is_master or release_in_title


def is_hotfix(pr):
    hotfix_in_head_branch_name = (
        "hotfix/" in pr["headRefName"].lower() or "hf/" in pr["headRefName"].lower()
    )
    hotfix_in_title = "hotfix" in pr["title"].lower()
    base_branch_is_production = "production" in pr["baseRefName"].lower()

    if not base_branch_is_production:
        return False

    return hotfix_in_head_branch_name or hotfix_in_title


def is_merge_back_from_prod(pr):
    base_branch_is_master = (
        "master" in pr["baseRefName"].lower() or "main" in pr["baseRefName"].lower()
    )
    head_branch_is_production = "production" in pr["headRefName"].lower()
    return base_branch_is_master and head_branch_is_production


def exclude_closeds(prs_list):
    return [pr for pr in prs_list if not is_closed(pr)]


def exclude_releases(prs_list):
    return [pr for pr in prs_list if not is_release(pr)]


def exclude_hotfixes(prs_list):
    return [pr for pr in prs_list if not is_hotfix(pr)]


def exclude_merge_backs_from_prod(prs_list):
    return [pr for pr in prs_list if not is_merge_back_from_prod(pr)]


def exclude_authors_in_list(prs_list, authors):
    return [pr for pr in prs_list if not get_author_login(pr) in authors]


def filter_valid_prs(prs_list, include_hotfixes=False, exclude_authors=[]):
    valid_prs_list = exclude_closeds(prs_list)
    valid_prs_list = exclude_releases(valid_prs_list)
    valid_prs_list = exclude_merge_backs_from_prod(valid_prs_list)

    if not include_hotfixes:
        valid_prs_list = exclude_hotfixes(valid_prs_list)

    if exclude_authors:
        valid_prs_list = exclude_authors_in_list(valid_prs_list, exclude_authors)
    return valid_prs_list


def filter_hotfixes(prs_list, exclude_authors=[]):
    valid_prs_list = exclude_closeds(prs_list)
    valid_prs_list = exclude_releases(valid_prs_list)
    valid_prs_list = exclude_merge_backs_from_prod(valid_prs_list)
    valid_prs_list = [pr for pr in prs_list if is_hotfix(pr)]

    if exclude_authors:
        valid_prs_list = exclude_authors_in_list(valid_prs_list, exclude_authors)
    return valid_prs_list


def format_timedelta(timedelta):
    if timedelta.total_seconds() < 0:
        return "Invalid timeframe"

    days = timedelta.days
    hours, remainder = divmod(timedelta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days} days {hours} hours {minutes} minutes"


def get_weekend_count(start_at, end_at):
    day_count = end_at.day - start_at.day
    number_of_complete_weeks = day_count // 7
    weekends = number_of_complete_weeks * 2

    additional_days = day_count % 7

    days_index = []
    for i in range(0, additional_days):
        day = start_at + datetime.timedelta(days=i)
        days_index.append(day.weekday())

    if 5 in days_index:
        weekends += 1
    if 6 in days_index:
        weekends += 1

    return weekends


def get_time_without_weekend(start_at, end_at):
    weekend_count = get_weekend_count(start_at, end_at)
    timedelta = end_at - start_at
    return timedelta - datetime.timedelta(days=weekend_count)
