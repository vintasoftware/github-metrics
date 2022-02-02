from github_metrics.helpers import filter_valid_prs


def count_prs(pr_list, include_hotfixes, exclude_authors, filter_authors):
    if not exclude_authors:
        exclude_authors = []
    prs_list = filter_valid_prs(pr_list, include_hotfixes, exclude_authors, filter_authors)

    print(
        f"     \033[1mPRs Count\033[0m"
        f"     ----------------------------------"
        f"     Total PRs counted: {len(prs_list)}"
    )
