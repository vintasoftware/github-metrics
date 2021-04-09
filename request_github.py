import requests
from requests.auth import HTTPBasicAuth
from time import sleep

from common import extract_datetime_or_none
from settings import GITHUB_LOGIN, GITHUB_TOKEN, REPOSITORY_NAME, ORG_NAME


def format_request_for_github(cursor=None):
    after = ""
    if cursor:
        after = f', after: "{cursor}"'

    return """{{
    organization(login: "{ORG_NAME}") {{
        repository(name: "{REPOSITORY_NAME}") {{
            pullRequests(
                first: 100,
                orderBy: {{
                    field: CREATED_AT,
                    direction: DESC
                }}{after}
            ) {{
                pageInfo {{
                    endCursor
                    startCursor
                    hasNextPage
                }}
                nodes {{
                    id
                    title
                    createdAt
                    baseRefName
                    headRefName
                    additions
                    deletions
                    reviews(first: 10) {{
                        nodes {{
                            createdAt
                            state
                            author {{
                                login
                            }}
                        }}
                    }}
                    author {{
                        login
                    }}
                    mergedAt
                    closedAt
                    commits(first: 10) {{
                        edges {{
                            node {{
                                commit {{
                                    oid
                                    message
                                    committedDate
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}
}}""".format(
        after=after, ORG_NAME=ORG_NAME, REPOSITORY_NAME=REPOSITORY_NAME
    )


def pr_was_created_between(pr, start_date, end_date):
    open_date = extract_datetime_or_none(pr.get("createdAt"))
    return open_date >= start_date and open_date <= end_date


def fetch_prs_between(start_date, end_date):
    prs_list = []
    current_date = None
    cursor = None
    has_next_page = True
    while has_next_page and (not current_date or current_date > start_date):
        response = requests.post(
            "https://api.github.com/graphql",
            auth=HTTPBasicAuth(GITHUB_LOGIN, GITHUB_TOKEN),
            json={"query": format_request_for_github(cursor)},
        )
        data = response.json().get("data")

        if not data:
            has_next_page = False
            continue

        organization = data.get("organization")
        if not organization:
            has_next_page = False
            continue

        repository = organization.get("repository")
        if not repository:
            has_next_page = False
            continue

        prs = repository.get("pullRequests")
        if not prs:
            has_next_page = False
            continue

        page_info = prs.get("pageInfo")
        if not page_info:
            has_next_page = False
            continue

        has_next_page = page_info["hasNextPage"]
        cursor = page_info["endCursor"]

        page_prs_list = prs.get("nodes")
        if not page_prs_list:
            has_next_page = False
            continue

        current_date = extract_datetime_or_none(page_prs_list[-1]["createdAt"])
        prs_list += [
            pr
            for pr in page_prs_list
            if pr_was_created_between(pr, start_date, end_date)
        ]
        sleep(1)

    return prs_list
