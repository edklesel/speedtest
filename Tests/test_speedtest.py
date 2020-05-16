import unittest
from Speedtest.speedtest import get_results

class TestSpeedtest(unittest.TestCase):

    def test_getresults(self):

        results = get_results()

        try:
            float(results[0])
        except (AttributeError, TypeError):
            raise AssertionError('Download value should be a float.')

        try:
            float(results[1])
        except (AttributeError, TypeError):
            raise AssertionError('Upload value should be a float.')

        self.assertTrue(type(results[2]) is str)

        self.assertTrue(len(results) == 3, msg=f"len(results)={len(results)}")