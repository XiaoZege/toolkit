"""toolkit 的测试。"""

from pathlib import Path

import pytest

from toolkit import chdir, log_call, retry, timer


def test_timer_returns_result_and_prints(capsys):
    @timer
    def add(a, b):
        return a + b

    assert add(1, 2) == 3
    out = capsys.readouterr().out
    assert "[timer]" in out
    assert "add" in out


def test_timer_keeps_function_name():
    @timer
    def add(a, b):
        return a + b

    assert add.__name__ == "add"


def test_retry_succeeds_after_failures():
    calls = {"n": 0}

    @retry(times=3, delay=0)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ValueError("还没好")
        return "好了"

    assert flaky() == "好了"
    assert calls["n"] == 3


def test_retry_gives_up_and_raises():
    @retry(times=2, delay=0)
    def always_fail():
        raise ValueError("一直失败")

    with pytest.raises(ValueError):
        always_fail()


def test_log_call_prints_around_function(capsys):
    @log_call
    def add(a, b):
        return a + b

    assert add(1, 2) == 3
    out = capsys.readouterr().out
    assert "进入 add" in out
    assert "离开 add" in out


def test_log_call_still_raises(capsys):
    @log_call
    def boom():
        raise ValueError("炸了")

    with pytest.raises(ValueError):
        boom()
    assert "ValueError" in capsys.readouterr().out


def test_chdir_switches_and_restores(tmp_path, monkeypatch):
    old = tmp_path / "old"
    old.mkdir()
    monkeypatch.chdir(old)

    with chdir(tmp_path):
        assert Path.cwd() == tmp_path

    assert Path.cwd() == old
