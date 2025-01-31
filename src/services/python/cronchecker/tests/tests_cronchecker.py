import unittest
from datetime import datetime
from cronchecker import is_time_matching_cron


## This checker only supports classical cron notation with 5 field
##
## * * * * * 
## | | | | |  
## | | | | | 
## | | | | +---- Day of the Week   (range: 1-7, 1 standing for Monday)
## | | | +------ Month of the Year (range: 1-12)
## | | +-------- Day of the Month  (range: 1-31)
## | +---------- Hour              (range: 0-23)
## +------------ Minute            (range: 0-59)
##

class TestCronChecker(unittest.TestCase):

    def test_every_minute(self):
        cron_expression = "* * * * *"
        test_time = datetime(2023, 10, 1, 12, 34)
        self.assertTrue(is_time_matching_cron(cron_expression, test_time))

    def test_specific_minute(self):
        cron_expression = "34 * * * *"
        test_time = datetime(2023, 10, 1, 12, 34)
        self.assertTrue(is_time_matching_cron(cron_expression, test_time))

        test_time = datetime(2023, 10, 1, 12, 35)
        self.assertFalse(is_time_matching_cron(cron_expression, test_time))

    def test_every_five_minutes(self):
        cron_expression = "*/5 * * * *"
        test_times = [
            datetime(2023, 10, 1, 12, 0),
            datetime(2023, 10, 1, 12, 5),
            datetime(2023, 10, 1, 12, 10)
        ]
        for test_time in test_times:
            with self.subTest(test_time=test_time):
                self.assertTrue(is_time_matching_cron(cron_expression, test_time))

        test_time = datetime(2023, 10, 1, 12, 6)
        self.assertFalse(is_time_matching_cron(cron_expression, test_time))

    def test_missing_argument_returns_function(self):
        # if no time is specified, the function uses datetime.now
        cron_expression = '* * * * *'
        self.assertIn(is_time_matching_cron(cron_expression), {True, False}, "The function should return either True or False.")

    def test_always_matches(self):
        cron_expression = "* * * * *"
        self.assertTrue(is_time_matching_cron(cron_expression, datetime.now()))

    def test_long_and_short_notations(self):
        date1 = datetime(year=2018, month=7, day=25, hour=15, minute=20)  # July is month 7 in Python datetime, Wednesday
        # Check long and short notations
        with self.assertRaises(Exception) as context:
          is_time_matching_cron('25 20 15 25 3 2018', date1)
          self.assertEqual(str(context.exception), "ValueError: Cron string must have exactly 5 fields.")
        with self.assertRaises(Exception) as context:
          is_time_matching_cron('25 20 15', date1)
          self.assertEqual(str(context.exception), "ValueError: Cron string must have exactly 5 fields.")
        # Short
        self.assertTrue(is_time_matching_cron('20 15 25 7 *', date1))
        self.assertFalse(is_time_matching_cron('20 15 25 7 1', date1)) #Monday
        self.assertFalse(is_time_matching_cron('20 15 25 7 2', date1)) #Tuesday
        self.assertTrue(is_time_matching_cron('20 15 25 7 3', date1)) #Wednesday
        self.assertFalse(is_time_matching_cron('20 15 25 7 4', date1)) #Thursday
        self.assertFalse(is_time_matching_cron('20 15 25 7 5', date1)) #Friday
        self.assertFalse(is_time_matching_cron('20 15 25 7 6', date1)) #Saturday
        self.assertFalse(is_time_matching_cron('20 15 25 7 7', date1)) #Soinday
        self.assertFalse(is_time_matching_cron('20 14 25 3 *', date1))

    def test_wildcards(self):
        date1 = datetime(2018, 7, 25, 15, 20)
        date2 = datetime(2019, 7, 25, 15, 20)

        # Check *
        self.assertTrue(is_time_matching_cron('20 15 25 7 3', date1))
        self.assertFalse(is_time_matching_cron('20 15 25 7 3', date2))
        self.assertTrue(is_time_matching_cron('20 15 25 7 *', date1))
        self.assertTrue(is_time_matching_cron('20 15 25 7 *', date2))
        self.assertTrue(is_time_matching_cron('20 15 25 * 3', date1))
        self.assertTrue(is_time_matching_cron('20 15 * 7 3', date1))
        self.assertTrue(is_time_matching_cron('20 * 25 7 3', date1))
        self.assertTrue(is_time_matching_cron('* 15 25 7 3', date1))

    def test_comma(self):
        date1 = datetime(2018, 7, 25, 15, 20)
        date2 = datetime(2017, 6, 24, 14, 19)

        # Check ,
        self.assertTrue(is_time_matching_cron('19,20 14,15 24,25 6,7 3,6', date1))
        self.assertTrue(is_time_matching_cron('19,20 14,15 24,25 6,7 3,6', date2))
        self.assertFalse(is_time_matching_cron('20,21 14,15 24,25 6,7 3,6', date2))

    def test_dash(self):
        date1 = datetime(2018, 7, 25, 15, 20)
        date2 = datetime(2017, 6, 24, 14, 19)
        date3 = datetime(2016, 5, 23, 13, 18)
        date4 = datetime(2024, 5, 23, 13, 18)
        # Check -
        self.assertTrue(is_time_matching_cron('18-20 13-15 23-25 5-7 1-3,6', date1))
        self.assertTrue(is_time_matching_cron('18-20 13-15 23-25 5-7 1-3,6', date2))
        self.assertTrue(is_time_matching_cron('18-20 13-15 23-25 5-7 1-3,6', date3))

        self.assertTrue(is_time_matching_cron('18-20 13-15 23-25 5-7 1-3,6', date3))
        self.assertFalse(is_time_matching_cron('18-20 13-15 23-25 5-7 1-3,6', date4))

        self.assertTrue(is_time_matching_cron('18-20,30 13-15 23-25 5-7 1-3', date1))
        self.assertTrue(is_time_matching_cron('18-20 13-15,17 23-25 5-7 1-3', date1))
        self.assertTrue(is_time_matching_cron('18-20 13-15 23-25,12 5-7 1-3', date1))
        self.assertTrue(is_time_matching_cron('18-20 13-15 23-25 5-7,9 1-3', date1))

    def test_slash(self):
        date1 = datetime(2018, 7, 25, 15, 20)

        # Check /
        self.assertTrue(is_time_matching_cron('*/2 */5 */5 5/2 1/2', date1))
        self.assertTrue(is_time_matching_cron('20/1 15/5 3/11 5/2 1/2', date1))

    def test_array(self):
        date1 = datetime(2018, 7, 25, 15, 20)

        # Check with array logic
        self.assertFalse(is_time_matching_cron('21 * * * *', date1))
        self.assertTrue(is_time_matching_cron('20 * * * *', date1))
        cron_expressions = ['20 * * * *', '21 * * * *']
        self.assertTrue(any(is_time_matching_cron(expr, date1) for expr in cron_expressions))

if __name__ == "__main__":
    unittest.main()