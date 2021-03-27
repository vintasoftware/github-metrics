import unittest
import arrow
import datetime

from tests.mocks import request_mock
from fetch_prs_mtm import get_merged_prs, format_prs_list
from helpers import filter_valid_prs


class TestPRsMTM(unittest.TestCase):
    def test_get_merged_prs_successfully(self):
        prs_list = [
            {"merged_at": None},
            {"merged_at": datetime.datetime(2021, 3, 25, 14, 28, 52)},
        ]
        merged_prs_list = get_merged_prs(prs_list)
        self.assertEqual(len(merged_prs_list), 1)


if __name__ == "__main__":
    unittest.main()