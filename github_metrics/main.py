from typing import Optional

import arrow
from fastapi import FastAPI

from github_metrics.metrics.time_to_merge import get_time_to_merge_data
from github_metrics.metrics.time_to_open import get_time_to_open_data
from github_metrics.metrics.time_to_review import get_time_to_review_data
from github_metrics.request import fetch_prs_between

app = FastAPI()


@app.get("/api/metrics/{metric}")
def read_item(
    metric: str,
    start_date: str,
    end_date: str,
    include_hotfixes: Optional[bool] = False,
    exclude_weekends: Optional[bool] = True,
    exclude_author: Optional[str] = None,
    filter_author: Optional[str] = None,
):
    start = arrow.get(start_date)
    end = arrow.get(f"{end_date}T23:59:59")

    pr_list = fetch_prs_between(start, end)

    if metric == "ttm":
        data = get_time_to_merge_data(
            pr_list,
            include_hotfixes,
            exclude_author,
            filter_author,
            exclude_weekends,
        )

        return {
            "metric": metric,
            "mean": data["mean"],
            "median": data["median"],
            "percentile_95": data["percentile_95"],
            "prs_list": data["merged_prs"],
        }

    if metric == "tto":
        data = get_time_to_open_data(
            pr_list,
            include_hotfixes,
            exclude_author,
            filter_author,
            exclude_weekends,
        )

        return {
            "metric": metric,
            "mean": data["mean"],
            "median": data["median"],
            "percentile_95": data["percentile_95"],
            "prs_list": data["total_prs"],
        }

    if metric == "ttr":
        data = get_time_to_review_data(
            pr_list,
            include_hotfixes,
            exclude_author,
            filter_author,
            exclude_weekends,
        )

        return {
            "metric": metric,
            "mean": data["mean"],
            "median": data["median"],
            "percentile_95": data["percentile_95"],
            "prs_list": data["total_prs"],
            "unreviewed_prs": data["unreviewed_prs"],
            "prs_over_24h": data["prs_over_24h"],
        }
