import argparse

from crawler_package.data_args import DataArgs


class ArgParse:
    """Реализация парсера консоли"""
    def __init__(self, args):
        self.parser = argparse.ArgumentParser(description='This is crawler without indexing.\n'
                                                          'Example of using: python3.8 ')
        self.args = args
        self.add_options()

    def add_options(self):
        self.parser.add_argument('sites', nargs='+', type=str,
                                 help='Sites from which the crawler will work (there may be one or more)')
        self.parser.add_argument('-d', type=int, default=3,
                                 help='The number of transitions in depth from a given page')

    def parse(self):
        parametrs = self.parser.parse_args(self.args)
        return DataArgs(parametrs.sites, parametrs.d)
