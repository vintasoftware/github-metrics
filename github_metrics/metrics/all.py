from github_metrics.metrics.time_to_merge import call_mean_time_to_merge_statistics
from github_metrics.metrics.time_to_review import calulate_prs_review_time_statistics
from github_metrics.metrics.time_to_open import call_time_to_open_statistics
from github_metrics.metrics.open_to_merge import (
    calulate_prs_open_to_merge_time_statistics,
)
from github_metrics.metrics.merge_rate import call_merge_rate_statistics
from github_metrics.metrics.pr_size import call_pr_size_statistics
from github_metrics.metrics.hotfixes_count import count_hotfixes


def call_all_metrics(
    pr_list, include_hotfixes, exclude_authors, filter_authors, exclude_weekends
):
    call_mean_time_to_merge_statistics(
        pr_list, include_hotfixes, exclude_authors, filter_authors, exclude_weekends
    )
    calulate_prs_review_time_statistics(
        pr_list, include_hotfixes, exclude_authors, filter_authors, exclude_weekends
    )
    call_time_to_open_statistics(
        pr_list, include_hotfixes, exclude_authors, filter_authors, exclude_weekends
    )
    calulate_prs_open_to_merge_time_statistics(
        pr_list, include_hotfixes, exclude_authors, filter_authors, exclude_weekends
    )
    call_merge_rate_statistics(
        pr_list, include_hotfixes, exclude_authors, filter_authors
    )
    call_pr_size_statistics(pr_list, include_hotfixes, exclude_authors, filter_authors)
    count_hotfixes(pr_list, exclude_authors, filter_authors)
