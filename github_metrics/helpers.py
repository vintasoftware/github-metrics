from .common import get_author_login
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


def exclude_closeds(pr_list):
    return [pr for pr in pr_list if not is_closed(pr)]


def exclude_releases(pr_list):
    return [pr for pr in pr_list if not is_release(pr)]


def exclude_hotfixes(pr_list):
    return [pr for pr in pr_list if not is_hotfix(pr)]


def exclude_merge_backs_from_prod(pr_list):
    return [pr for pr in pr_list if not is_merge_back_from_prod(pr)]


def exclude_authors_in_list(pr_list, authors):
    return [pr for pr in pr_list if not get_author_login(pr) in authors]


def filter_authors_in_list(pr_list, authors):
    return [pr for pr in pr_list if get_author_login(pr) in authors]


def filter_valid_prs(pr_list, include_hotfixes, exclude_authors, filter_authors):
    valid_pr_list = exclude_closeds(pr_list)
    valid_pr_list = exclude_releases(valid_pr_list)
    valid_pr_list = exclude_merge_backs_from_prod(valid_pr_list)

    if not include_hotfixes:
        valid_pr_list = exclude_hotfixes(valid_pr_list)
    if exclude_authors:
        valid_pr_list = exclude_authors_in_list(valid_pr_list, exclude_authors)
    if filter_authors:
        valid_pr_list = filter_authors_in_list(valid_pr_list, filter_authors)
    return valid_pr_list


def filter_hotfixes(pr_list, exclude_authors, filter_authors):
    valid_pr_list = exclude_closeds(pr_list)
    valid_pr_list = exclude_releases(valid_pr_list)
    valid_pr_list = exclude_merge_backs_from_prod(valid_pr_list)
    valid_pr_list = [pr for pr in pr_list if is_hotfix(pr)]

    if exclude_authors:
        valid_pr_list = exclude_authors_in_list(valid_pr_list, exclude_authors)
    if filter_authors:
        valid_pr_list = filter_authors_in_list(valid_pr_list, filter_authors)

    return valid_pr_list


def format_timedelta(timedelta):
    if timedelta.total_seconds() < 0:
        return "Invalid timeframe"

    days = timedelta.days
    hours, remainder = divmod(timedelta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days} days {hours} hours {minutes} minutes"


def get_weekend_time(start_at, end_at):
    day_count = end_at.date() - start_at.date()
    weekends = datetime.timedelta()
    for i in range(0, day_count.days + 1):
        day = start_at + datetime.timedelta(days=i)

        # 5 represents Saturday and 6 represents Sunday
        if day.weekday() == 5 or day.weekday() == 6:
            # In a time period, if it's starting a time count, count from the beginning until end of day
            if i == 0:
                weekends += (
                    datetime.datetime(day.year, day.month, day.day, 23, 59, 59) - day
                )

            # If it's the end of a time period, count from start of day until the end time
            elif i == day_count.days:
                weekends += end_at - datetime.datetime(day.year, day.month, day.day)

            else:
                weekends += datetime.timedelta(days=1)
    return weekends


def get_time_without_weekend(start_at, end_at):
    weekend_timedelta = get_weekend_time(start_at, end_at)
    timedelta = end_at - start_at
    return timedelta - weekend_timedelta
