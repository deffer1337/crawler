import argparse
import sys
from pathlib import Path

import requests

from modules.crawler_package.data_args import DataArgs
from modules.crawler_package.url_manager import is_not_correct_url
from modules.utils import get_msg_if_response_not_ok

DEFAULT_THREADS = 200


class ArgParse:
    """Console parser for crawler"""

    def __init__(self, args):
        self.parser = argparse.ArgumentParser(description="This is crawler without indexing.\n")
        self.args = args
        self._add_options()

    def _add_options(self):
        self.parser.add_argument(
            "sites", nargs="+", type=str, help="Sites from which the crawler will work (separated by a space)"
        )

        self.parser.add_argument("-d", type=int, default=3, help="The number of transitions in depth from a given page")

        self.parser.add_argument(
            "-t",
            nargs="+",
            type=int,
            default=[],
            help="The numbers of threads for downloading each corresponding pages" "(separated by a space)",
        )

        self.parser.add_argument("-a", action="store_true", help="Saving all pages to the archive.")

        self.parser.add_argument(
            "-p",
            default=Path(Path(__file__).resolve().parent.parent.parent, "Pages"),
            type=str,
            help="The path to the folder where all downloaded pages will be saved. "
            'By default, the "Pages" folder is created in the current project.',
        )

    def parse(self) -> DataArgs:
        """
        Parsing console arguments
        :return: DataArgs
        """
        parameters = self.parser.parse_args(self.args)
        if not Path(parameters.p).exists():
            raise ValueError(
                f"Path does not exists. \n"
                f"Trying crawl {parameters.sites} with incorrect argument: path = {parameters.p}"
            )
        if parameters.d < 1:
            raise ValueError(
                f"Depth should be more then 0. \n"
                f"Trying crawl {parameters.sites} with incorrect argument: depth = {parameters.d}"
            )
        if len(parameters.t) > len(parameters.sites):
            raise ValueError(
                "The number of threads is specified for a larger "
                "number of pages than the transmitted ones. \n"
                f"Trying crawl {len(parameters.sites)} sites: {parameters.sites} "
                f"with incorrect number of threads = {len(parameters.t)}"
            )

        for site in parameters.sites:
            is_not_correct_url_msg = is_not_correct_url(site)
            if is_not_correct_url_msg:
                print(is_not_correct_url_msg)
                sys.exit()
            response_not_ok_msg = get_msg_if_response_not_ok(requests.get(site))
            if response_not_ok_msg:
                print(f"{response_not_ok_msg}")
                sys.exit()

        count_threads = len(parameters.sites) - len(parameters.t)
        for i in range(count_threads):
            parameters.t.append(DEFAULT_THREADS)

        return DataArgs(parameters.sites, parameters.d, parameters.t, parameters.p, parameters.a)
