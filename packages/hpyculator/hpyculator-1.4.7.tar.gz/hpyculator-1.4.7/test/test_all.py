import tempfile
from typing import Any

import pytest

from hpyculator import hpycore

test_reflect: Any = 0  # 初始化一个变量，用于检测结果


@pytest.mark.run(order=2)
def test_all():
    with tempfile.TemporaryFile("w+t", encoding="utf-8", errors="ignore") as filestream:
        assert hpycore.setIoInstance(filestream) is None
        assert filestream is hpycore.getIoInstance()

        assert hpycore.addOne(1) == 2

        assert hpycore.setOutPutData(12) is None
        assert hpycore.getOutputData() == 12

        assert hpycore.write("test", end="test") is None
        assert hpycore.write_without_flush("test", end="test") is None
        assert hpycore.flush() is None
        filestream.seek(0)
        assert filestream.read() == "testtesttesttest"

    hpycore.output("test")
    assert test_reflect == "test"
    hpycore.clearOutput()
    assert test_reflect == 0
    hpycore.setOutput("test")
    assert test_reflect == "test"

    assert get_fun_name(1, 2, c=3) == (6, "get_fun_name")
    assert get_fun_runtime()[0] == 12

@hpycore.funName
def get_fun_name(a, b, __fun_name__, c=1):
    return (a + b + c, __fun_name__)


@hpycore.reRunTimes(12)
def get_fun_runtime():
    return 12
