import unittest
from tests.request_mock import prs_list_mock
from helpers import filter_valid_prs


class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.prs_list = prs_list_mock

    def test_filter_valid_prs_successfully(self):
        valid_prs_list = filter_valid_prs(self.prs_list)
        self.assertEqual(len(valid_prs_list), 1)


if __name__ == "__main__":
    unittest.main()