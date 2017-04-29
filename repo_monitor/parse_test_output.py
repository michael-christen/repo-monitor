from xml.etree import ElementTree as ET


def get_total_coverage(filename='coverage.xml'):
    '''Get coverage percentage of a repository from the output of pytest.'''
    tree = ET.parse(filename)
    root = tree.getroot()
    return float(root.attrib['line-rate'])


class NosetestData(object):
    def __init__(self, data):
        root = ET.fromstring(data)
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
    with open(filename, 'r') as f:
        return NosetestData(f.read())
