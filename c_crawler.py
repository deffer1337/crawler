import logging
import os
import sys
import json
import time
from multiprocessing import Process
from pathlib import Path
from typing import Union, List

from modules.crawler_package.crawler import Crawler
from modules.crawler_package.arg_parse import ArgParse
from modules.infrastructure.file_manager import FileManager
from modules.infrastructure.program_state import ProgramState
from modules.utils import get_answer_yes_or_no


def _get_crawler_states(states: List[str], path_to_directory_with_states: Union[str, Path]):
    crawler_states = []
    for state in states:
        path_to_store_file = Path(path_to_directory_with_states, state)
        path_to_store_backup = Path(path_to_directory_with_states, f'{state}~')
        try:
            crawler_state = ProgramState(path_to_store_backup, path_to_store_file).get_state_json()
            crawler_states.append(crawler_state)
        except json.JSONDecodeError as e:
            logger.error(f'This state file {path_to_store_file} not json.')
            sys.stdout.write(f'This state file {path_to_store_file} not json. Remove it?[Y/n]')
            answer = get_answer_yes_or_no()

            if answer:
                logger.info(f'State file {path_to_store_file} removed.')
                os.remove(path_to_store_file)

    return crawler_states


def _crash_recovery(path_to_directory_with_states: Union[str, Path]):
    states = ProgramState.get_states_from_directory(path_to_directory_with_states)
    if states:
        logger.critical(f'Crawling of {data_args.sites} interrupted. You have unfinished states: {states}')
        sys.stdout.write(f'You have unfinished crawling with domains {states}.\n'
                         f'Do you want to finish running the program with these domains?[Y/n]')
        answer = get_answer_yes_or_no()

        if answer:
            crawler_states = _get_crawler_states(states, path_to_directory_with_states)
            processes = []
            for crawler_state in crawler_states:
                try:
                    _args = (crawler_state.get('url'), crawler_state.get('depth'),
                             crawler_state.get('count_threads'), crawler_state.get('sites'),
                             crawler_state.get('path'), crawler_state.get('is_archive_option'),
                             crawler_state)
                except KeyError as key_error_msg:
                    logger.error(f'State {crawler_state.get_name_store_file()} not correct. \n'
                                 f'The argument key {str(key_error_msg)} of the saved state '
                                 f'doesn\'t match the required argument key')
                    sys.stdout.write(
                        f'State {crawler_state.get_name_store_file()} not correct. Remove this state?[Y/n]')
                    answer = get_answer_yes_or_no()
                    if answer:
                        crawler_state.delete_state()
                        logger.info(f'Incorrect state {crawler_state.get_name_store_file()} removed.')

                    continue

                proc = Process(target=crawler.start, args=_args)

                processes.append(proc)
                logger.info(f'Crawling of {states} continued.')
                proc.start()

            for process in processes:
                process.join()


if __name__ == '__main__':
    FileManager.make_directory_if_not_exist(Path(__file__).resolve().parent, 'Pages')
    FileManager.make_directory_if_not_exist(Path(__file__).resolve().parent, 'States')
    logger = logging.getLogger('crawl')
    start = time.perf_counter()
    try:
        data_args = ArgParse(sys.argv[1:]).parse()
        logger.info(f'Start crawling {data_args.sites} with depth = {data_args.depth}, '
                    f'count_threads = {data_args.count_threads}, path = {data_args.path} '
                    f'and archive_option is {data_args.is_archive_option}')
    except ValueError as value_error_msg:
        logger.critical(f'{str(value_error_msg)}')
        print(value_error_msg)
        sys.exit()

    crawler = Crawler()
    _crash_recovery(Path(Path(__file__).resolve().parent, 'States'))
    processes = []
    for i in range(len(data_args.sites)):
        proc = Process(target=crawler.start, args=(data_args.sites[i], data_args.depth, data_args.count_threads[i],
                                                   data_args.sites, data_args.path, data_args.is_archive_option,))
        processes.append(proc)
        proc.start()

    for process in processes:
        process.join()

    logger.info(f'Crawling ended in {time.perf_counter() - start} seconds.')
    print(f'Crawling ended in {time.perf_counter() - start} seconds')
