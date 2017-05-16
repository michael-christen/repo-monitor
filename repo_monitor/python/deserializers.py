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
    def __init__(self, package=None, raw_json=None, mi_json=None):
        self.paths = [package]
        self.raw_json = raw_json
        self.mi_json = mi_json
        raw_dict = self._get_raw_dict()
        self.metric_dict = {
            'lloc': self._get_sum_metric_from_raw_dict(raw_dict, 'lloc'),
            'mi': self._get_weighted_mi(raw_dict),
        }
        # Attempt to make cyclomatic complexity if possible
        try:
            self.metric_dict['cc'] = self._get_average_cc()
        except Exception:
            pass

    def _get_raw_dict(self):
        if self.raw_json is None:
            self.raw_json = RawHarvester(self.paths, Config(
                exclude=None,
                ignore=None,
            )).as_json()
        return json.loads(self.raw_json)

    def _get_mi_dict(self):
        if self.mi_json is None:
            self.mi_json = MIHarvester(self.paths, Config(
                min='A',
                max='F',
                multi=True,
                exclude=None,
                ignore=None,
                show=True,
            )).as_json()
        return json.loads(self.mi_json)

    def _get_sum_metric_from_raw_dict(self, raw_dict, metric):
        sum_metrics = defaultdict(int)
        for f_name, raw_value in raw_dict.iteritems():
            for k, v in raw_value.iteritems():
                sum_metrics[k] += v
        return sum_metrics[metric]

    def _get_average_cc(self):
        cc_data = CCHarvester(self.paths, Config(
            min='A',
            max='F',
            exclude=None,
            ignore=None,
            order=cc_mod.SCORE,
            no_assert=False,
            show_closures=False,
        ))
        # Copy CCHarvestor
        total_cc = 0.0
        analyzed = 0
        for name, blocks in cc_data.results:
            if 'error' in blocks:
                continue
            _, cc, n = cc_to_terminal(blocks, True, 'A', 'F', True)
            total_cc += cc
            analyzed += n
        return total_cc / analyzed

    def _get_weighted_mi(self, raw_dict):
        mi_dict = self._get_mi_dict()
        total_mi = 0
        total_lloc = 0
        for f_name, mi_value in mi_dict.iteritems():
            cur_lloc = raw_dict[f_name]['lloc']
            total_mi += mi_value['mi'] * cur_lloc
            total_lloc += cur_lloc
        return total_mi / (total_lloc + 0.0)
