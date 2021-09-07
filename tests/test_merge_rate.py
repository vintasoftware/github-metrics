import datetime
import unittest

from github_metrics.metrics.merge_rate import (
    call_merge_rate_statistics,
    get_merged_prs,
    get_prs_authors,
)


class TestPRsMTM(unittest.TestCase):
    def test_get_merged_prs_successfully(self):
        pr_list = [
            {"merged_at": None},
            {"merged_at": datetime.datetime(2021, 3, 25, 14, 28, 52)},
        ]
        merged_pr_list = get_merged_prs(pr_list)
        self.assertEqual(merged_pr_list, [pr_list[1]])

    def test_no_prs_to_calculate_mr(self):
        message = call_merge_rate_statistics([])

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
