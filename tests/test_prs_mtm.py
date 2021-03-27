import unittest
from datetime import timedelta

from tests.mocks import request_mock
from fetch_prs_mtm import get_merged_prs, format_prs_list
from helpers import filter_valid_prs


class TestPRsMTM(unittest.TestCase):
    def test_get_merged_prs_successfully(self):
        valid_prs = format_prs_list(filter_valid_prs(request_mock))
        merged_prs_list = get_merged_prs(valid_prs)
        self.assertEqual(len(merged_prs_list), 2)


if __name__ == "__main__":
    unittest.main()