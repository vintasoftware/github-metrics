import unittest
from unittest import mock
import datetime

from tests.mocks import request_mock
from mr import get_merged_prs, get_prs_authors
from helpers import filter_valid_prs


class TestPRsMTM(unittest.TestCase):
    def test_get_merged_prs_successfully(self):
        prs_list = [
            {"merged_at": None},
            {"merged_at": datetime.datetime(2021, 3, 25, 14, 28, 52)},
        ]
        merged_prs_list = get_merged_prs(prs_list)
        self.assertEqual(merged_prs_list, [prs_list[1]])

    def test_get_authors_list(self):
        prs = [
            {
                "author": {"login": "ladygaga"},
            },
            {
                "author": {"login": "beyonce"},
            },
            {
                "author": {"login": "badgalriri"},
            },
        ]

        prs_authors = get_prs_authors(prs)
        self.assertEqual(
            prs_authors,
            ["ladygaga", "beyonce", "badgalriri"],
        )


if __name__ == "__main__":
    unittest.main()