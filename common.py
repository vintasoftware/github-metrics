import arrow


def extract_datetime_or_none(isoformat_str_date):
    if not isoformat_str_date:
        return arrow.now().shift(days=1000)

    try:
        arrow_date = arrow.get(isoformat_str_date)
    except Exception:
        return arrow.now().shift(days=1000)

    return arrow_date.datetime


def get_author_login(pr_or_review):
    author = pr_or_review.get("author")
    if not author:
        return

    return author.get("login")