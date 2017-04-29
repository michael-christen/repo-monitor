import os
import unittest

from ..deserializers import get_total_coverage
from ..deserializers import parse_nosetest_output
from ..parsers import NosetestParser


def _get_data_filename(filename):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'data/{}'.format(filename))


EXAMPLE_TEST_XML = '''
<?xml version="1.0" encoding="utf-8"?>
<testsuite errors="0" failures="0" name="pytest" skips="0" tests="5" time="0.138">
    <testcase
        classname="file_kvstore.tests.test_basic.TestBasic"
        file="file_kvstore/tests/test_basic.py"
        line="30"
        name="test_add"
        time="1.5000000001"></testcase>
    <testcase
        classname="file_kvstore.tests.test_basic.TestBasic"
        file="file_kvstore/tests/test_basic.py"
        line="51"
        name="test_format"
        time="0.023"><system-out>a: 5.123 h: hello </system-out></testcase>
    <testcase
        classname="file_kvstore.tests.test_basic.TestBasic"
        file="file_kvstore/tests/test_basic.py"
        line="37"
        name="test_order"
        time="0.13"></testcase>
    <testcase
        classname="file_kvstore.tests.test_basic.TestBasic"
        file="file_kvstore/tests/test_basic.py"
        line="44"
        name="test_replace"
        time="10.23"></testcase>
    <testcase
        classname="file_kvstore.tests.test_basic.TestBasic"
        file="file_kvstore/tests/test_basic.py"
        line="23"
        name="test_start"
        time="0.00015"></testcase></testsuite>
'''  # noqa


class TestCoverage(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(
            0.883,
            get_total_coverage(_get_data_filename('test_coverage.xml')))


class TestTests(unittest.TestCase):
    def compare_dicts(self, dict1, dict2):
        for test_name, expected_time in dict1.viewitems():
            try:
                actual_time = dict2[test_name]
            except KeyError:
                self.fail(
                    "{} expected, but not found in:\n{}".format(
                        test_name, dict2.keys()))
            self.assertAlmostEqual(expected_time, actual_time, delta=0.0001)
        self.assertEqual(
            set(dict2.keys()),
            set(dict1.keys()))

    def test_basic(self):
        self.maxDiff = None
        nosetest_data = parse_nosetest_output(
            _get_data_filename('test_nosetests.xml'))
        self.assertEqual(5, nosetest_data.num_tests)
        self.assertEqual(0.138, nosetest_data.time)
        expected_test2time = {
            'file_kvstore.tests.test_basic.TestBasic:test_add': 1.5,
            'file_kvstore.tests.test_basic.TestBasic:test_format': 0.023,
            'file_kvstore.tests.test_basic.TestBasic:test_order': 0.13,
            'file_kvstore.tests.test_basic.TestBasic:test_start': 0.00015,
            'file_kvstore.tests.test_basic.TestBasic:test_replace': 10.23,
        }
        self.compare_dicts(expected_test2time, nosetest_data.test2time)

    def test_nosetest_parser(self):
        file_arg = '--file={}'.format(_get_data_filename('test_nosetests.xml'))
        self.assertEqual('0.138', NosetestParser().run(['time', file_arg]))
        self.assertEqual('5', NosetestParser().run(['num_tests', file_arg]))
        self.assertEqual(5,
                         len(NosetestParser().run(['test2time',
                             file_arg]).split('\n')))
