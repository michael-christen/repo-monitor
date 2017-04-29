import argparse
import sys

from .parse_test_output import get_total_coverage
from .parse_test_output import NosetestData


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
        nosetest_data = NosetestData(data)
        metric = getattr(nosetest_data, parsed_args.metric)
        if isinstance(metric, dict):
            for k, v in metric.viewitems():
                print k, v
        else:
            print metric
        return metric


class Parser(object):
    def __init__(self):
        self.base_parser = argparse.ArgumentParser(
            description='Retrieve information from test runs',
        )
        self.sub_commands = {
            'coverage_py': CoverageParser,
            'nosetest_py': NosetestParser,
        }
        self.base_parser.add_argument(
            'cmd',
            choices=self.sub_commands.keys(),
            help='Command to use')

    def run(self, args=None):
        args = args or sys.argv[1:]
        command = self.base_parser.parse_args(args[:1]).cmd
        self.sub_commands[command]().run(args[1:])


def main():
    parser = Parser()
    parser.run()