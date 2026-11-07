# toolkit

写给自己用的 Python 小工具包。四样东西：计时、重试、记录调用、临时切目录。

## 里面有什么

- `timer`：打印函数花了多少秒
- `retry`：失败自动重试，最多几次、间隔多久自己定
- `log_call`：进函数、出函数、抛出错误时各打一行
- `chdir`：临时切换工作目录，出了 `with` 块自动切回

## 用法

```python
from toolkit import timer, retry

@timer
def slow_sum(n):
    return sum(range(n))

@retry(times=3, delay=0.5)
def fetch():
    ...
```

## 开发

```
uv sync
uv run pytest
```
