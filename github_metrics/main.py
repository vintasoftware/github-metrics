import arrow
from fastapi import FastAPI

from github_metrics.metrics.time_to_merge import get_time_to_merge_data
from github_metrics.request import fetch_prs_between

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/metrics/{metric}")
def read_item(metric: str, start_date: str, end_date: str):
    start = arrow.get(start_date)
    end = arrow.get(f"{end_date}T23:59:59")

    pr_list = fetch_prs_between(start, end)

    data = get_time_to_merge_data(pr_list)

    return {
        "metric": metric,
        "mean": data["mean"],
        "median": data["median"],
        "percentile_95": data["percentile_95"],
        "merged_prs": data["merged_prs"],
    }
