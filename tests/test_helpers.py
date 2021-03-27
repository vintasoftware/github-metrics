import unittest
from datetime import timedelta

from tests.mocks import request_mock
from helpers import filter_valid_prs, format_timedelta


class TestHelpers(unittest.TestCase):
    def test_filter_valid_prs_successfully(self):
        valid_prs_list = filter_valid_prs(request_mock)
        self.assertEqual(len(valid_prs_list), 4)

    def test_format_time_string(self):
        time = timedelta(seconds=1 * 24 * 60 * 60 + 48035)
        formatted_time = format_timedelta(time)

        hours, remainder = divmod(time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.assertEqual(
            formatted_time, f"{time.days} days {hours} hours {minutes} minutes"
        )

    def test_negative_timedelta_format_time_returns_invalid(self):
        time = timedelta(seconds=1 * 24 * 60 * 60 + 48035)
        formatted_time = format_timedelta(-time)

        self.assertEqual(formatted_time, "Invalid timeframe")


if __name__ == "__main__":
    unittest.main()