from collections import namedtuple
from xml.etree import ElementTree as ET


def get_total_coverage(filename='coverage.xml'):
    '''Get coverage percentage of a repository from the output of pytest.'''
    tree = ET.parse(filename)
    root = tree.getroot()
    return float(root.attrib['line-rate'])


NosetestData = namedtuple('NosetestData', ['num_tests', 'time', 'test2time'])
class NosetestData(object):
    def __init__(self, filename='test-output/nosetests.xml'):
        tree = ET.parse(filename)
        root = tree.getroot()
        assert root.tag == 'testsuite'
        self.time = float(root.attrib['time'])
        self.num_tests = int(root.attrib['tests'])
        self.test2time = {}
        for test_case in root:
            assert test_case.tag == 'testcase'
            test_name = '{}:{}'.format(
                test_case.attrib['classname'], test_case.attrib['name'])
            self.test2time[test_name] = float(test_case.attrib['time'])
        assert self.num_tests == len(self.test2time)


def parse_nosetest_output(filename='test-output/nosetests.xml'):
    return NosetestData(filename=filename)
