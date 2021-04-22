import numpy

from common import extract_datetime_or_none, get_author_login
from helpers import filter_valid_prs, format_timedelta
from request_github import fetch_prs_between


def count_hotfixes(start_date, end_date, exclude_authors=None):
    if not exclude_authors:
        exclude_authors = []

    prs_list = fetch_prs_between(start_date, end_date, label="Hotfix")
    valid_prs_list = filter_valid_prs(
        prs_list, include_hotfixes=True, exclude_authors=exclude_authors
    )
    

    print(
        f"""
            \033[1mHotfixes Count\033[0m
            ----------------------------------
            Total PRs counted: {len(valid_prs_list)}
            """
    )
