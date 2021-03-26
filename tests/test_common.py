import unittest
from datetime import timedelta

from tests.request_mock import prs_list_mock
from common import extract_datetime_or_none


class TestCommon(unittest.TestCase):
    def test_extract_datetime(self):
        isoformat_str_date = "2021-03-25T21:19:45Z"
        datetime = extract_datetime_or_none(isoformat_str_date)
        self.assertNotEqual(datetime, None)

    def test_fails_extracting_datetime(self):
        isoformat_str_date = "2021-03-25T21!"
        datetime = extract_datetime_or_none(isoformat_str_date)
        self.assertEqual(datetime, None)


if __name__ == "__main__":
    unittest.main()