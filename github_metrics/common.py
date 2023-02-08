import arrow


def extract_datetime_or_none(isoformat_str_date):
    try:
        arrow_date = arrow.get(isoformat_str_date)
    except Exception:
        return None

    return arrow_date.datetime


def get_author_login(pr_or_review):
    author = pr_or_review.get("author")
    if not author:
        return None

    return author.get("login")


def get_reviews_from_pr(pr):
    reviews_root = pr.get("reviews")

    if not reviews_root:
        return []

    reviews = reviews_root.get("nodes", [])
    if not reviews:
        return []

    return reviews

def _get_raw_ready_datetime_from_pr(pr):
    timeline_root = pr.get("timelineItems", {})
    if not timeline_root:
        return pr["createdAt"]

    timeline = timeline_root.get("edges", [])
    if not timeline or not timeline[0]:
        return pr["createdAt"]

    timeline_node = timeline[0].get("node")
    if not timeline_node:
        return pr["createdAt"]

    return timeline_node.get("createdAt", pr["createdAt"])

def get_ready_datetime_from_pr(pr):
    return extract_datetime_or_none(_get_raw_ready_datetime_from_pr(pr))
