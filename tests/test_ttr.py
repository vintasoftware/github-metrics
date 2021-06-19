import unittest
import datetime

from github_metrics.metrics.ttr import (
    filter_reviewed_prs,
    filter_prs_with_more_than_24h_before_review,
)


class TestPRsMTR(unittest.TestCase):
    def test_filter_reviewed_prs_successfully(self):
        prs_list = [
            {"first_review_at": None},
            {"first_review_at": datetime.datetime(2021, 3, 25, 14, 28, 52)},
        ]
        reviewed_prs = filter_reviewed_prs(prs_list)
        self.assertEqual(reviewed_prs, [prs_list[1]])

    def test_filter_prs_with_more_than_18h_before_review(self):
        prs_list = [
            {
                "created_at": datetime.datetime(2021, 3, 25, 14, 28, 52),
                "first_review_at": None,
            },
            {
                "created_at": datetime.datetime(2021, 3, 2, 10, 10),
                "first_review_at": datetime.datetime(2021, 3, 4, 15, 12),
            },
            {
                "created_at": datetime.datetime(2021, 3, 2, 10, 10),
                "first_review_at": datetime.datetime(2021, 3, 2, 11, 3),
            },
        ]

        prs_list = filter_prs_with_more_than_24h_before_review(prs_list)
        self.assertEqual(len(prs_list), 2)


if __name__ == "__main__":
    unittest.main()
