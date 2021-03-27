import unittest
from unittest import mock
import datetime

from tests.mocks import request_mock
from fetch_prs_mtm import get_merged_prs, call_mean_time_to_merge_statistics
from helpers import filter_valid_prs


class TestPRsMTM(unittest.TestCase):
    def test_get_merged_prs_successfully(self):
        prs_list = [
            {"merged_at": None},
            {"merged_at": datetime.datetime(2021, 3, 25, 14, 28, 52)},
        ]
        merged_prs_list = get_merged_prs(prs_list)
        self.assertEqual(len(merged_prs_list), 1)

    @mock.patch("fetch_prs_mtm.fetch_prs_between")
    def test_no_prs_to_calculate_mtm(self, mock_fetch_prs_between):
        mock_fetch_prs_between.return_value = []
        message = call_mean_time_to_merge_statistics("2020", "2021")

        self.assertEqual(
            message,
            "There are no valid PRs to pull this data from, please select another timeframe",
        )


if __name__ == "__main__":
    unittest.main()