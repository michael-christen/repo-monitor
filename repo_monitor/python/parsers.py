import argparse

from .deserializers import CoverageDeserializer
from .deserializers import NosetestDeserializer
from .deserializers import RadonDeserializer


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
        with open(parsed_args.file, 'r') as f:
            line_rate = CoverageDeserializer(f.read()).line_rate
        format_string = '{:.' + str(parsed_args.num_decimals) + 'f}%'
        coverage_string = format_string.format(100 * line_rate)
        print coverage_string
        return coverage_string


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
        output_str = ''
        if isinstance(metric, dict):
            test_list = ['{} {}'.format(k, v) for k, v in metric.viewitems()]
            output_str = '\n'.join(test_list)
        else:
            output_str = '{}'.format(metric)
        print output_str
        return output_str


class RadonParser(object):
    def __init__(self):
        self.base_parser = argparse.ArgumentParser(
            description='Get Code Quality Metrics',
        )
        self.base_parser.add_argument(
            'metric',
            choices=['lloc', 'cc', 'mi'],
            help='Metric to gather')
        self.base_parser.add_argument(
            '--package',
            help='Package to inspect. (Needed for cc).')
        self.base_parser.add_argument(
            '--raw_json',
            help='JSON file with raw Radon metrics')
        self.base_parser.add_argument(
            '--mi_json',
            help='JSON file with maintanability index Radon metrics')

    def _read_file_if_available(self, file_name):
        if file_name is None:
            return None
        with open(file_name, 'r') as f:
            return f.read()

    def run(self, args):
        parsed_args = self.base_parser.parse_args(args)
        radon_data = RadonDeserializer(
            package=parsed_args.package,
            raw_json=self._read_file_if_available(parsed_args.raw_json),
            mi_json=self._read_file_if_available(parsed_args.mi_json),
        ).metric_dict
        if parsed_args.metric == 'lloc':
            format_str = '{:d}'
        else:
            format_str = '{:0.2f}'
        output_str = format_str.format(radon_data[parsed_args.metric])
        print output_str
        return output_str
