import os
import unittest

from ..parse_test_output import get_total_coverage
from ..parse_test_output import parse_nosetest_output


def _get_data_filename(filename):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'data/{}'.format(filename))


class TestCoverage(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(
            0.883,
            get_total_coverage(_get_data_filename('coverage.xml')))


class TestTests(unittest.TestCase):
    def test_basic(self):
        self.maxDiff = None
        nosetest_data = parse_nosetest_output(
            _get_data_filename('nosetests.xml'))
        self.assertEqual(5, nosetest_data.num_tests)
        self.assertEqual(0.138, nosetest_data.time)
        expected_test2time = {
            'file_kvstore.tests.test_basic.TestBasic:test_add': 1.5,
            'file_kvstore.tests.test_basic.TestBasic:test_format': 0.023,
            'file_kvstore.tests.test_basic.TestBasic:test_order': 0.13,
            'file_kvstore.tests.test_basic.TestBasic:test_start': 0.00015,
            'file_kvstore.tests.test_basic.TestBasic:test_replace': 10.23,
        }
        for test_name, expected_time in expected_test2time.viewitems():
            try:
                actual_time = nosetest_data.test2time[test_name]
            except KeyError:
                self.fail(
                    "{} expected, but not found in:\n{}".format(
                        test_name, nosetest_data.test2time.keys()))
            self.assertAlmostEqual(expected_time, actual_time, delta=0.0001)
        self.assertEqual(
            set(nosetest_data.test2time.keys()),
            set(expected_test2time.keys()))
