from common import extract_datetime_or_none, get_author_login
from helpers import filter_valid_prs
from request_github import fetch_prs_between


def format_prs_list(prs_list):
    return [
        {
            "author": get_author_login(pr),
            "merged_at": extract_datetime_or_none(pr.get("mergedAt"))
            if pr.get("mergedAt")
            else None,
        }
        for pr in prs_list
    ]


def get_merged_prs(formatted_prs_list):
    merged_prs = []

    for pr in formatted_prs_list:
        if pr["merged_at"] is not None:
            merged_prs.append(pr)
    return merged_prs


def get_prs_authors(prs_list):
    pr_author_list = []

    for pr in prs_list:
        if pr["author"] not in pr_author_list:
            pr_author_list.append(pr["author"])
    return pr_author_list


def call_merge_rate_statistics(
    start_date, end_date, include_hotfixes=False, exclude_authors=[]
):
    prs_list = fetch_prs_between(start_date, end_date)
    valid_prs_list = filter_valid_prs(
        prs_list, include_hotfixes=include_hotfixes, exclude_authors=exclude_authors
    )
    formatted_prs_list = format_prs_list(valid_prs_list)
    merged_prs = get_merged_prs(formatted_prs_list)
    if not merged_prs or merged_prs == []:
        return "There are no valid PRs to pull this data from, please select another timeframe"

    prs_authors = get_prs_authors(merged_prs)
    merge_rate = len(merged_prs) / len(prs_authors)

    print(
        f"""
            \033[1mMerge Rate\033[0m
            ----------------------------------
            Total PRs calculated: {len(merged_prs)}
            Total devs calculated: {len(prs_authors)}
            ----------------------------------
            Merge Rate: {merge_rate}
            """
    )
