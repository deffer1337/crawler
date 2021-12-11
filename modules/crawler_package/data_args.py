from dataclasses import dataclass
from typing import List


@dataclass
class DataArgs:
    """
    Console args for crawler
    """
    sites: List[str]
    depth: int
    count_threads: List[int]
    path: str
    is_archive_option: bool
