import unittest
from pathlib import Path

from modules.crawler_package.arg_parse import ArgParse
from modules.crawler_package.data_args import DataArgs


class TestArgParse(unittest.TestCase):
    def test_parse_when_wrong_path_then_raise_value_error(self):
        with self.assertRaises(ValueError) as error:
            args = ['https://tproger.ru/', '-p', f'{Path(__file__).resolve().parent}/124']
            ArgParse(args).parse()

        self.assertTrue(f'Path does not exists. \n'
                        f'Trying crawl [\'https://tproger.ru/\'] with incorrect argument: path = '
                        f'{Path(__file__).resolve().parent}/124' in str(error.exception))

    def test_parse_when_wrong_depth_then_raise_value_error(self):
        with self.assertRaises(ValueError) as error:
            args = ['https://tproger.ru/', '-d', '-1']
            ArgParse(args).parse()

        self.assertTrue(f'Depth should be more then 0. \n'
                        f'Trying crawl [\'https://tproger.ru/\'] with incorrect argument: depth = -1'
                        in str(error.exception))

    def test_parse_when_wrong_numberOfThreads_then_raise_value_error(self):
        with self.assertRaises(ValueError) as error:
            args = ['https://tproger.ru/', '-t', '100', '2500']
            ArgParse(args).parse()

        self.assertTrue('The number of threads is specified for a larger '
                        'number of pages than the transmitted ones. \n'
                        f'Trying crawl 1 sites: [\'https://tproger.ru/\'] '
                        f'with incorrect number of threads = 2' in str(error.exception))

    def test_parse_when_wrong_url_then_system_exit(self):
        with self.assertRaises(SystemExit):
            args = ['https://tproggger.ru/']
            ArgParse(args).parse()

    def test_parse_when_right_url_and_depth(self):
        args = ['https://tproger.ru/', '-d', '5', '-t', '1000', '-a']
        data_args = DataArgs(sites=['https://tproger.ru/'], depth=5, count_threads=[1000],
                             path=f'{Path(__file__).resolve().parent.parent}/Pages', is_archive_option=True)
        returns_data_args = ArgParse(args).parse()
        returns_data_args.path = str(returns_data_args.path)
        self.assertEqual(data_args, returns_data_args)
