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


def call_pr_size_statistics(pr_list, include_hotfixes, exclude_authors, filter_authors):
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

    print(
        f"""
            \033[1mPull Requests Size\033[0m
            ----------------------------------
            Total PRs calculated: {len(formatted_pr_list)}
            ----------------------------------
            Total Lines Mean: {round(total_mean, 2)} lines
            Total Lines Median: {round(total_median, 2)} lines
            Total Lines 95 percentile: {round(total_percentile, 2)} lines

            Diff Rate Mean: {round(rate_mean, 2)}
            Diff Rate Median: {round(rate_median, 2)}
            Diff Rate 95 percentile: {round(rate_percentile, 2)}
            """
    )
