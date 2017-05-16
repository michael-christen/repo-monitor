import os
import unittest

from ..deserializers import CoverageDeserializer
from ..deserializers import NosetestDeserializer

from ..parsers import NosetestParser
from ..parsers import RadonParser


def _get_data_filename(filename):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'data/{}'.format(filename))


class TestCoverageDeserializer(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(
            0.883,
            CoverageDeserializer(EXAMPLE_COVERAGE_XML).line_rate)


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
        nosetest_data = NosetestDeserializer(EXAMPLE_TEST_XML)
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


class TestRadon(unittest.TestCase):
    def test_radon_parser(self):
        base_args = [
            '--raw_json={}'.format(_get_data_filename('test_raw_radon.json')),
            '--mi_json={}'.format(_get_data_filename('test_mi_radon.json')),
        ]
        self.assertEqual('192', RadonParser().run(base_args + ['lloc']))
        self.assertEqual('54.34', RadonParser().run(base_args + ['mi']))


EXAMPLE_COVERAGE_XML = '''<?xml version="1.0" ?>
<coverage branch-rate="0" line-rate="0.883" timestamp="1493359236075" version="4.0.3">
	<!-- Generated by coverage.py: https://coverage.readthedocs.org -->
	<!-- Based on https://raw.githubusercontent.com/cobertura/web/f0366e5e2cf18f111cbd61fc34ef720a6584ba02/htdocs/xml/coverage-03.dtd -->
	<sources>
		<source>/home/michael/projects/scripts/file-kvstore</source>
		<source>/home/michael/projects/scripts/file-kvstore/file_kvstore</source>
	</sources>
	<packages>
		<package branch-rate="0" complexity="0" line-rate="0.8036" name="file_kvstore">
			<classes>
				<class branch-rate="0" complexity="0" filename="file_kvstore/__init__.py" line-rate="1" name="__init__.py">
					<methods/>
					<lines/>
				</class>
				<class branch-rate="0" complexity="0" filename="file_kvstore/constants.py" line-rate="1" name="constants.py">
					<methods/>
					<lines>
						<line hits="1" number="1"/>
					</lines>
				</class>
				<class branch-rate="0" complexity="0" filename="file_kvstore/io.py" line-rate="0.7083" name="io.py">
					<methods/>
					<lines>
						<line hits="1" number="1"/>
					</lines>
				</class>
				<class branch-rate="0" complexity="0" filename="file_kvstore/parser.py" line-rate="0.8889" name="parser.py">
					<methods/>
					<lines>
						<line hits="1" number="1"/>
					</lines>
				</class>
				<class branch-rate="0" complexity="0" filename="file_kvstore/utils.py" line-rate="0.8462" name="utils.py">
					<methods/>
					<lines>
						<line hits="0" number="19"/>
					</lines>
				</class>
			</classes>
		</package>
		<package branch-rate="0" complexity="0" line-rate="1" name="file_kvstore.tests">
			<classes>
				<class branch-rate="0" complexity="0" filename="file_kvstore/tests/__init__.py" line-rate="1" name="__init__.py">
					<methods/>
					<lines/>
				</class>
				<class branch-rate="0" complexity="0" filename="file_kvstore/tests/test_basic.py" line-rate="1" name="test_basic.py">
					<methods/>
					<lines>
						<line hits="1" number="1"/>
						<line hits="1" number="2"/>
						<line hits="1" number="4"/>
					</lines>
				</class>
			</classes>
		</package>
	</packages>
</coverage>
'''  # noqa


EXAMPLE_TEST_XML = '''<?xml version="1.0" encoding="utf-8"?>
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
