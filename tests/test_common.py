import unittest

from tests.mocks import request_mock
from common import extract_datetime_or_none, get_author_login, get_reviews_from_pr


class TestCommon(unittest.TestCase):
    def setUp(self):
        self.pr = request_mock[1]
        self.empty_pr = {
            "id": "",
            "title": "",
            "createdAt": "",
            "baseRefName": "",
            "headRefName": "",
            "reviews": {},
            "author": None,
            "mergedAt": None,
            "closedAt": None,
            "commits": {},
        }

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
        author = get_author_login(self.empty_pr)

        self.assertEqual(author, None)

    def test_get_reviews_from_pr_successfully(self):
        reviews = get_reviews_from_pr(self.pr)
        self.assertEqual(self.pr.get("reviews").get("nodes"), reviews)

    def test_pr_without_review(self):
        reviews = get_reviews_from_pr(self.empty_pr)
        self.assertEqual(reviews, [])


if __name__ == "__main__":
    unittest.main()
