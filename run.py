import sys
import arrow

from fetch_prs_mtm import call_mean_time_to_merge_statistics
from fetch_prs_review_time import calulate_prs_review_time_statistics


def run():
    metric = sys.argv[1]
    start_date = arrow.get(sys.argv[2])
    end_date = arrow.get(sys.argv[3])

    if sys.argv[1] == "mtm":
        call_mean_time_to_merge_statistics(start_date, end_date)
    elif sys.argv[1] == "mtr":
        calulate_prs_review_time_statistics(start_date, end_date)


run()