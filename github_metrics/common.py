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
