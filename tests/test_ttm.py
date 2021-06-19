import unittest
import datetime

from tests.mocks import request_mock
from github_metrics.metrics.ttm import (
    get_merged_prs,
    call_mean_time_to_merge_statistics,
)


class TestPRsMTM(unittest.TestCase):
    def test_get_merged_prs_successfully(self):
        pr_list = [
            {"merged_at": None},
            {"merged_at": datetime.datetime(2021, 3, 25, 14, 28, 52)},
        ]
        merged_pr_list = get_merged_prs(pr_list)
        self.assertEqual(merged_pr_list, [pr_list[1]])

    def test_no_prs_to_calculate_mtm(self):
        message = call_mean_time_to_merge_statistics([])

        self.assertEqual(
            message,
            "There are no valid PRs to pull this data from, please select another timeframe",
        )


if __name__ == "__main__":
    unittest.main()
