import unittest
from datetime import timedelta

from tests.request_mock import prs_list_mock
from common import extract_datetime_or_none, get_author_login, get_reviews_from_pr


class TestCommon(unittest.TestCase):
    def setUp(self):
        self.pr = prs_list_mock[0]

    def test_extract_datetime_successfully(self):
        isoformat_str_date = self.pr.get("createdAt")
        datetime = extract_datetime_or_none(isoformat_str_date)
        self.assertNotEqual(datetime, None)

    def test_fails_extracting_datetime(self):
        isoformat_str_date = "2021-03-25T21!"
        datetime = extract_datetime_or_none(isoformat_str_date)
        self.assertEqual(datetime, None)

    def test_gets_author_login_successfully(self):
        author = get_author_login(self.pr)
        self.assertEqual(author, self.pr.get("author").get("login"))

    def test_fails_getting_author_login(self):
        authorless_pr = {
            "id": "",
            "title": "",
            "createdAt": "",
            "baseRefName": "master",
            "headRefName": "",
            "reviews": {},
            "author": None,
            "mergedAt": None,
            "closedAt": None,
            "commits": {},
        }
        author = get_author_login(authorless_pr)

        self.assertEqual(author, None)


if __name__ == "__main__":
    unittest.main()