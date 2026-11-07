"""一个临时切换工作目录的上下文管理器。"""

import os
from collections.abc import Iterator
from contextlib import contextmanager


@contextmanager
def chdir(path: str | os.PathLike[str]) -> Iterator[None]:
    """临时切到 path，出了 with 块自动切回原来的目录。"""
    old = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)
