"""三个常用装饰器：计时、重试、记录调用。"""

import functools
import time
from collections.abc import Callable
from typing import Any


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """打印函数执行花了多少秒。"""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        cost = time.perf_counter() - start
        print(f"[timer] {func.__name__} 用了 {cost:.4f} 秒")
        return result

    return wrapper


def retry(
    times: int = 3,
    delay: float = 0.5,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """失败就重试，最多 times 次，每次间隔 delay 秒。"""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[retry] 第 {attempt} 次失败：{e}")
                    if attempt == times:
                        raise
                    time.sleep(delay)

        return wrapper

    return decorator


def log_call(func: Callable[..., Any]) -> Callable[..., Any]:
    """进函数打一行，出函数打一行，出错也打一行。"""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"[log] 进入 {func.__name__}，参数：{args} {kwargs}")
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(f"[log] {func.__name__} 抛了 {type(e).__name__}: {e}")
            raise
        print(f"[log] 离开 {func.__name__}，返回：{result!r}")
        return result

    return wrapper
