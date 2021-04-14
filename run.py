import sys
import arrow

from ttm import call_mean_time_to_merge_statistics
from ttr import calulate_prs_review_time_statistics
from mr import call_merge_rate_statistics
from pr_size import call_pr_size_statistics


def run():
    include_hotfixes = False
    user_list = []
    metric = ""
    for arg in sys.argv:
        if "metric=" in arg:
            metric = arg.split("metric=")[1]
        elif "start_date=" in arg:
            start_date = arg.split("start_date=")[1]
            start_date = arrow.get(start_date)
        elif "end_date=" in arg:
            end_date = arg.split("end_date=")[1]
            end_date = arrow.get(end_date)
        elif "--include-hotfixes" in arg:
            include_hotfixes = True
        elif "exclude=" in arg:
            users = arg.split("exclude=")[1]
            user_list = users.split(",")

    if metric == "ttm":
        call_mean_time_to_merge_statistics(
            start_date, end_date, include_hotfixes, user_list
        )
    elif metric == "ttr":
        calulate_prs_review_time_statistics(
            start_date, end_date, include_hotfixes, user_list
        )
    elif metric == "mr":
        call_merge_rate_statistics(start_date, end_date, include_hotfixes, user_list)
    elif metric == "pr_size":
        call_pr_size_statistics(start_date, end_date, include_hotfixes, user_list)


run()