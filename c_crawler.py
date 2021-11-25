import sys
import time
from multiprocessing import Process
from pathlib import Path

from crawler_package.crawler import Crawler
from crawler_package.arg_parse import ArgParse
from infrastructure.file_manager import FileManager

if __name__ == '__main__':
    FileManager.make_directory_if_not_exist(Path(__file__).resolve().parent, 'Pages')
    FileManager.make_directory_if_not_exist(Path(__file__).resolve().parent, 'Logs')
    start = time.perf_counter()
    try:
        data_args = ArgParse(sys.argv[1:]).parse()
    except ValueError as value_error_msg:
        print(value_error_msg)
        sys.exit()

    crawler = Crawler()
    processes = []
    for i in range(len(data_args.sites)):
        proc = Process(target=crawler.start, args=(data_args.sites[i], data_args.depth, data_args.count_threads[i],
                                                   data_args.sites, data_args.path, data_args.is_archive_option, ))
        processes.append(proc)
        proc.start()

    for process in processes:
        process.join()

    print(f'Crowling ended in {time.perf_counter() - start} seconds')
