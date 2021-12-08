from dataclasses import dataclass
from typing import List


@dataclass
class DataArgs:
    sites: List[str]
    depth: int
    count_threads: List[int]
    path: str
    is_archive_option: bool
