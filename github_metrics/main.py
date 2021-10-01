from typing import Optional

import arrow
from fastapi import FastAPI, HTTPException

from github_metrics.metrics.hotfixes_count import get_hotfixes_data
from github_metrics.metrics.merge_rate import get_merge_rate_data
from github_metrics.metrics.open_to_merge import get_open_to_merge_time_data
from github_metrics.metrics.pr_size import get_pr_size_data
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

    if end > start:
        raise HTTPException(
            status_code=403, detail="Date range is not in chronological order"
        )

    pr_list = fetch_prs_between(start, end)

    if metric == "ttm":
        data = get_time_to_merge_data(
            pr_list=pr_list,
            include_hotfixes=include_hotfixes,
            exclude_author=exclude_author,
            filter_author=filter_author,
            exclude_weekends=exclude_weekends,
        )

        return {
            "metric": "Time to merge",
            "mean": data["mean"],
            "median": data["median"],
            "percentile_95": data["percentile_95"],
            "prs_list": data["merged_prs"],
        }

    elif metric == "tto":
        data = get_time_to_open_data(
            pr_list=pr_list,
            include_hotfixes=include_hotfixes,
            exclude_author=exclude_author,
            filter_author=filter_author,
            exclude_weekends=exclude_weekends,
        )

        return {
            "metric": "Time to open",
            "mean": data["mean"],
            "median": data["median"],
            "percentile_95": data["percentile_95"],
            "prs_list": data["total_prs"],
        }

    elif metric == "ttr":
        data = get_time_to_review_data(
            pr_list=pr_list,
            include_hotfixes=include_hotfixes,
            exclude_author=exclude_author,
            filter_author=filter_author,
            exclude_weekends=exclude_weekends,
        )

        return {
            "metric": "Time to review",
            "mean": data["mean"],
            "median": data["median"],
            "percentile_95": data["percentile_95"],
            "prs_list": data["total_prs"],
            "unreviewed_prs": data["unreviewed_prs"],
            "prs_over_24h": data["prs_over_24h"],
        }

    elif metric == "pr_size":
        data = get_pr_size_data(
            pr_list=pr_list,
            include_hotfixes=include_hotfixes,
            exclude_author=exclude_author,
            filter_author=filter_author,
        )

        return {
            "metric": "PR size",
            "prs_list": data["total_prs"],
            "total_mean": data["total_mean"],
            "total_median": data["total_median"],
            "total_percentile_95": data["total_percentile_95"],
            "rate_mean": data["rate_mean"],
            "rate_median": data["rate_median"],
            "rate_percentile_95": data["rate_percentile_95"],
        }

    elif metric == "otm":
        data = get_open_to_merge_time_data(
            pr_list=pr_list,
            include_hotfixes=include_hotfixes,
            exclude_author=exclude_author,
            filter_author=filter_author,
            exclude_weekends=exclude_weekends,
        )

        return {
            "metric": "Open to merge",
            "mean": data["mean"],
            "median": data["median"],
            "percentile_95": data["percentile_95"],
            "prs_list": data["total_prs"],
            "merged_pr_rate": data["merged_pr_rate"],
        }

    elif metric == "mr":
        data = get_merge_rate_data(
            pr_list=pr_list,
            include_hotfixes=include_hotfixes,
            exclude_author=exclude_author,
            filter_author=filter_author,
        )

        return {
            "metric": "Merge rate",
            "prs_list": data["total_prs"],
            "prs_authors": data["prs_authors"],
            "merge_rate": data["merge_rate"],
        }

    elif metric == "hotfixes_count":
        data = get_hotfixes_data(
            pr_list=pr_list, exclude_author=exclude_author, filter_author=filter_author
        )

        return {
            "metric": "Hotfix count",
            "hotfix_list": data["hotfix_list"],
        }

    else:
        raise HTTPException(status_code=403, detail="Item not found")
