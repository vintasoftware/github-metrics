import sys
import arrow

from ttm import call_mean_time_to_merge_statistics
from ttr import calulate_prs_review_time_statistics
from mr import call_merge_rate_statistics
from pr_size import call_pr_size_statistics


def run():
    metric = sys.argv[1]
    start_date = arrow.get(sys.argv[2])
    end_date = arrow.get(sys.argv[3])

    if sys.argv[1] == "ttm":
        call_mean_time_to_merge_statistics(start_date, end_date)
    elif sys.argv[1] == "ttr":
        calulate_prs_review_time_statistics(start_date, end_date)
    elif sys.argv[1] == "mr":
        call_merge_rate_statistics(start_date, end_date)
    elif sys.argv[1] == "pr_size":
        call_pr_size_statistics(start_date, end_date)


run()