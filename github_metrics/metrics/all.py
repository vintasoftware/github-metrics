from github_metrics.metrics.ttm import call_mean_time_to_merge_statistics
from github_metrics.metrics.ttr import calulate_prs_review_time_statistics
from github_metrics.metrics.tto import call_time_to_open_statistics
from github_metrics.metrics.mr import call_merge_rate_statistics
from github_metrics.metrics.pr_size import call_pr_size_statistics
from github_metrics.metrics.hotfixes_count import count_hotfixes


def call_all_metrics(pr_list, include_hotfixes, exclude_authors, exclude_weekends):
    call_mean_time_to_merge_statistics(
        pr_list, include_hotfixes, exclude_authors, exclude_weekends
    )
    calulate_prs_review_time_statistics(
        pr_list, include_hotfixes, exclude_authors, exclude_weekends
    )
    call_time_to_open_statistics(
        pr_list, include_hotfixes, exclude_authors, exclude_weekends
    )
    call_merge_rate_statistics(pr_list, include_hotfixes, exclude_authors)
    call_pr_size_statistics(pr_list, include_hotfixes, exclude_authors)
    count_hotfixes(pr_list, exclude_authors)
