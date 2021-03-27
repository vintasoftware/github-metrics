import unittest
import datetime

from fetch_prs_mtr import filter_reviewed_prs


class TestPRsMTR(unittest.TestCase):
    def test_filter_reviewed_prs_successfully(self):
        prs_list = [
            {"first_review_at": None},
            {"first_review_at": datetime.datetime(2021, 3, 25, 14, 28, 52)},
        ]
        reviewed_prs = filter_reviewed_prs(prs_list)
        self.assertEqual(reviewed_prs, [prs_list[1]])


if __name__ == "__main__":
    unittest.main()