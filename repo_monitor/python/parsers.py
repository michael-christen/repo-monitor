import argparse

from .deserializers import get_total_coverage
from .deserializers import NosetestDeserializer


class CoverageParser(object):
    def __init__(self):
        self.base_parser = argparse.ArgumentParser(
            description='Get Python Coverage',
        )
        self.base_parser.add_argument(
            '--file',
            default='coverage.xml',
            help='Coverage File')
        self.base_parser.add_argument(
            '--num_decimals',
            default=0,
            help='Number of decimals to output')

    def run(self, args):
        parsed_args = self.base_parser.parse_args(args)
        format_string = '{:.' + str(parsed_args.num_decimals) + 'f}%'
        print format_string.format(100 * get_total_coverage(parsed_args.file))


class NosetestParser(object):
    def __init__(self):
        self.base_parser = argparse.ArgumentParser(
            description='Get Python Test Output Metrics',
        )
        self.base_parser.add_argument(
            'metric',
            choices=['time', 'num_tests', 'test2time'],
            help='Metric to gather')
        self.base_parser.add_argument(
            '--file',
            default='nosetests.xml',
            help='Test Output File')

    def run(self, args):
        parsed_args = self.base_parser.parse_args(args)
        with open(parsed_args.file, 'r') as f:
            data = f.read()
        nosetest_data = NosetestDeserializer(data)
        metric = getattr(nosetest_data, parsed_args.metric)
        if isinstance(metric, dict):
            for k, v in metric.viewitems():
                print k, v
        else:
            print metric
        return metric
