import sys
import time
from multiprocessing import Process
from pathlib import Path

from crawler_package.crawler import Crawler
from crawler_package.arg_parse import ArgParse
from crawler_package.file_manager import FileManager

if __name__ == '__main__':
    FileManager.make_directory_if_not_exist(Path(Path(__file__).resolve().parent, 'Pages'))
    start = time.perf_counter()
    data_args = ArgParse(sys.argv[1:]).parse()
    crawler = Crawler()
    processes = []

    for site in data_args.sites:
        proc = Process(target=crawler.start, args=(site, data_args.depth,))
        processes.append(proc)
        proc.start()

    for process in processes:
        process.join()

    print(time.perf_counter() - start)
