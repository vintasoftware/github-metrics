import unittest
from unittest import mock
import datetime

from mr import get_merged_prs, get_prs_authors, call_merge_rate_statistics
from helpers import filter_valid_prs


class TestPRsMTM(unittest.TestCase):
    def test_get_merged_prs_successfully(self):
        prs_list = [
            {"merged_at": None},
            {"merged_at": datetime.datetime(2021, 3, 25, 14, 28, 52)},
        ]
        merged_prs_list = get_merged_prs(prs_list)
        self.assertEqual(merged_prs_list, [prs_list[1]])

    @mock.patch("mr.fetch_prs_between")
    def test_no_prs_to_calculate_mr(self, mock_fetch_prs_between):
        mock_fetch_prs_between.return_value = []
        message = call_merge_rate_statistics("2020", "2021")

        self.assertEqual(
            message,
            "There are no valid PRs to pull this data from, please select another timeframe",
        )

    def test_get_authors_list(self):
        prs = [
            {
                "author": "ladygaga",
            },
            {
                "author": "beyonce",
            },
            {
                "author": "badgalriri",
            },
            {
                "author": "badgalriri",
            },
        ]

        prs_authors = get_prs_authors(prs)
        self.assertEqual(
            prs_authors,
            ["ladygaga", "beyonce", "badgalriri"],
        )


if __name__ == "__main__":
    unittest.main()