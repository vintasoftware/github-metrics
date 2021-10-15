import numpy

from github_metrics.helpers import filter_valid_prs


def format_pr_list(pr_list):
    return [
        {
            "additions": pr["additions"],
            "deletions": pr["deletions"],
        }
        for pr in pr_list
    ]


def get_pr_size_data(pr_list, include_hotfixes, exclude_authors, filter_authors):
    valid_pr_list = filter_valid_prs(
        pr_list, include_hotfixes, exclude_authors, filter_authors
    )
    formatted_pr_list = format_pr_list(valid_pr_list)

    total_line_diff = []
    diff_line_rate = []

    for pr in formatted_pr_list:
        total_line_diff.append(pr["additions"] + pr["deletions"])
        diff_line_rate.append(pr["additions"] - pr["deletions"])

    total_mean = numpy.mean(total_line_diff)
    total_median = numpy.median(total_line_diff)
    total_percentile = numpy.percentile(total_line_diff, 95)

    rate_mean = numpy.mean(diff_line_rate)
    rate_median = numpy.median(diff_line_rate)
    rate_percentile = numpy.percentile(diff_line_rate, 95)

    return {
        "total_prs": formatted_pr_list,
        "total_mean": total_mean,
        "total_median": total_median,
        "total_percentile_95": total_percentile,
        "rate_mean": rate_mean,
        "rate_median": rate_median,
        "rate_percentile_95": rate_percentile,
    }


def call_pr_size_statistics(pr_list, include_hotfixes, exclude_authors, filter_authors):
    data = get_pr_size_data(
        pr_list=pr_list,
        include_hotfixes=include_hotfixes,
        exclude_authors=exclude_authors,
        filter_authors=filter_authors,
    )

    print(
        f"     \033[1mPull Requests Size\033[0m\n"
        f"     ----------------------------------\n"
        f"     Total PRs calculated: {len(data['formatted_pr_list'])}\n"
        f"     ----------------------------------\n"
        f"     Total Lines Mean: {round(data['total_mean'], 2)} lines\n"
        f"     Total Lines Median: {round(data['total_median'], 2)} lines\n"
        f"     Total Lines 95 percentile: {round(data['total_percentile'], 2)} lines\n\n"
        f"     Diff Rate Mean: {round(data['rate_mean'], 2)}\n"
        f"     Diff Rate Median: {round(data['rate_median'], 2)}\n"
        f"     Diff Rate 95 percentile: {round(data['rate_percentile'], 2)}\n"
    )
