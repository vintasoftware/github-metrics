from common import extract_datetime_or_none, get_author_login, get_reviews_from_pr


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


def filter_valid_prs(prs_list, include_hotfixes=True):
    valid_prs_list = exclude_merge_backs_from_prod(
        exclude_releases(exclude_closeds(prs_list))
    )

    if not include_hotfixes:
        valid_prs_list = exclude_hotfixes(valid_prs_list)

    return valid_prs_list


def format_timedelta(timedelta):
    if timedelta.total_seconds() < 0:
        return "Invalid timeframe"

    days = timedelta.days
    hours, remainder = divmod(timedelta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days} days {hours} hours {minutes} minutes"
