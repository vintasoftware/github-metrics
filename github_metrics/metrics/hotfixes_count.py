from github_metrics.helpers import filter_hotfixes


def count_hotfixes(pr_list, exclude_authors=None):
    if not exclude_authors:
        exclude_authors = []
    hotfix_list = filter_hotfixes(pr_list, exclude_authors=exclude_authors)

    print(
        f"""
            \033[1mHotfixes Count\033[0m
            ----------------------------------
            Total PRs counted: {len(hotfix_list)}
            """
    )
