from helpers import filter_hotfixes
from request_github import fetch_prs_between


def count_hotfixes(start_date, end_date, exclude_authors=None):
    if not exclude_authors:
        exclude_authors = []
    prs_list = fetch_prs_between(start_date, end_date)
    valid_prs_list = filter_hotfixes(
        prs_list, exclude_authors=exclude_authors
    )
    

    print(
        f"""
            \033[1mHotfixes Count\033[0m
            ----------------------------------
            Total PRs counted: {len(valid_prs_list)}
            """
    )
