import datetime
import unittest

from github_metrics.metrics.time_to_review import (
    filter_prs_with_more_than_24h_before_review,
    filter_reviewed_prs,
)


class TestPRsMTR(unittest.TestCase):
    def test_filter_reviewed_prs_successfully(self):
        pr_list = [
            {"first_review_at": None},
            {"first_review_at": datetime.datetime(2021, 3, 25, 14, 28, 52)},
        ]
        reviewed_prs = filter_reviewed_prs(pr_list)
        self.assertEqual(reviewed_prs, [pr_list[1]])

    def test_filter_prs_with_more_than_18h_before_review(self):
        pr_list = [
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

        pr_list = filter_prs_with_more_than_24h_before_review(pr_list)
        self.assertEqual(len(pr_list), 2)


if __name__ == "__main__":
    unittest.main()
