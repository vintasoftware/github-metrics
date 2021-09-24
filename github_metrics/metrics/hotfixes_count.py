from github_metrics.helpers import filter_hotfixes


def get_hotfixes_data(pr_list, exclude_authors, filter_authors):
    if not exclude_authors:
        exclude_authors = []
    hotfix_list = filter_hotfixes(pr_list, exclude_authors, filter_authors)
    return {"hotfix_list": hotfix_list}


def count_hotfixes(pr_list, exclude_authors, filter_authors):
    data = get_hotfixes_data(pr_list, exclude_authors, filter_authors)
    print(
        f"     \033[1mHotfixes Count\033[0m\n"
        f"     ----------------------------------\n"
        f"     Total PRs counted: {len(data['hotfix_list'])}\n"
    )
