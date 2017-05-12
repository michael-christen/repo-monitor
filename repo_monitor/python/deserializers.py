import json

from collections import defaultdict
from xml.etree import ElementTree as ET

from radon.cli import Config
from radon.cli.harvest import CCHarvester
from radon.cli.harvest import RawHarvester
from radon.cli.harvest import MIHarvester
from radon.cli.tools import cc_to_terminal
import radon.complexity as cc_mod


class CoverageDeserializer(object):
    def __init__(self, data):
        root = ET.fromstring(data)
        self.line_rate = float(root.attrib['line-rate'])


class NosetestDeserializer(object):
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


class RadonDeserializer(object):
    def __init__(self, package):
        paths = [package]
        raw_data = RawHarvester(paths, Config(
            exclude=None,
            ignore=None,
        ))
        raw_dict = json.loads(raw_data.as_json())
        sum_metrics = defaultdict(int)
        for f_name, raw_value in raw_dict.iteritems():
            for k, v in raw_value.iteritems():
                sum_metrics[k] += v
        lloc = sum_metrics['lloc']

        cc_data = CCHarvester(paths, Config(
            min='A',
            max='F',
            exclude=None,
            ignore=None,
            order=cc_mod.SCORE,
            no_assert=False,
            show_closures=False,
        ))
        # Copy CCHarvestor
        average_cc = 0.0
        analyzed = 0
        for name, blocks in cc_data.results:
            if 'error' in blocks:
                continue
            _, cc, n = cc_to_terminal(blocks, True, 'A', 'F', True)
            average_cc += cc
            analyzed += n
        cc = average_cc / analyzed

        mi_data = MIHarvester(paths, Config(
            min='A',
            max='F',
            multi=True,
            exclude=None,
            ignore=None,
            show=True,
        ))
        mi_dict = json.loads(mi_data.as_json())
        total_mi = 0
        total_lloc = 0
        for f_name, mi_value in mi_dict.iteritems():
            cur_lloc = raw_dict[f_name]['lloc']
            total_mi += mi_value['mi'] * cur_lloc
            total_lloc += cur_lloc
        weighted_mi = total_mi / (total_lloc + 0.0)

        self.metric_dict = {
            'lloc': lloc,
            'cc': cc,
            'mi': weighted_mi,
        }
