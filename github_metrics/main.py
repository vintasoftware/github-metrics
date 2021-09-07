from typing import Optional

import arrow
from fastapi import FastAPI

from github_metrics.metrics.time_to_merge import get_time_to_merge_data
from github_metrics.request import fetch_prs_between

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/metrics/{metric}")
def read_item(
    metric: str,
    start_date: str,
    end_date: str,
    include_hotfixes: Optional[bool] = False,
    exclude_weekends: Optional[bool] = True,
    exclude_authors: Optional[str] = None,
    filter_authors: Optional[str] = None,
):
    start = arrow.get(start_date)
    end = arrow.get(f"{end_date}T23:59:59")

    pr_list = fetch_prs_between(start, end)

    if metric == "ttm":
        data = get_time_to_merge_data(
            pr_list,
            include_hotfixes,
            exclude_authors,
            filter_authors,
            exclude_weekends,
        )

        return {
            "metric": metric,
            "mean": data["mean"],
            "median": data["median"],
            "percentile_95": data["percentile_95"],
            "merged_prs": data["merged_prs"],
        }
