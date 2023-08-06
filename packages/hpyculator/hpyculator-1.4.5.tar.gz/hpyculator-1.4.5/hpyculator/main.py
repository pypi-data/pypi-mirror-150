from typing import Callable, Tuple, Any

from .signal import main_window_signal

io_instance: open = None  # 我想用类属性的，但是时间给我干到原来的三倍，傻眼了


class Main:
    def __init__(self):
        self.STRING = (1 << 0)
        self.NUM = (1 << 1)
        self.FLOAT = (1 << 2)
        self.LIST = (1 << 3)

        self.ON = (1 << 1)
        self.OFF = (1 << 0)  # 因为没读到就用这个作为缺省，所以每个参数的(1<<0)就是缺省

        # 'output_mode'
        self.RETURN_ONCE = (1 << 0)
        self.RETURN_LIST = (1 << 1)
        self.RETURN_LIST_OUTPUT_IN_ONE_LINE = (1 << 2)
        self.NO_RETURN = (1 << 3)
        self.NO_RETURN_SINGLE_FUNCTION = (1 << 4)

    @staticmethod
    def write(anything, end="\n") -> None:
        """
        用于向指定的文件流写入，每次写入之后立即刷新缓存区（立即写入硬盘）

        :param anything: 要写入的东西
        :param end: 每次写入在末尾追加的东西，默认为换行符
        :return: None
        """
        global io_instance
        io_instance.write(str(anything) + end)
        io_instance.flush()
        return None

    @staticmethod
    def write_without_flush(anything, end="\n") -> None:
        """
        用于向指定的文件流写入，每次写入之后不刷新缓存区，需要手动刷新（使用flush函数）

        :param anything: 要写入的东西
        :param end: 每次写入在末尾追加的东西，默认为换行符
        :return: None
        """
        global io_instance
        io_instance.write(str(anything) + end)
        return None

    @staticmethod
    def flush() -> None:
        """
        用于刷新缓存区（将缓存区中的数据写入硬盘）

        :return: None
        """
        global io_instance
        io_instance.flush()
        return None

    @staticmethod
    def output(anything) -> None:
        """
        输出到框体

        :param anything: 要输出到框体的数据
        :return: None
        """
        main_window_signal.appendOutPutBox.emit(str(anything))
        return None

    @staticmethod
    def clearOutput() -> None:
        """
        清空输出框

        :return: None
        """
        main_window_signal.clearOutPutBox.emit()
        return None

    @staticmethod
    def setOutput(msg: str) -> None:
        """
        设置输出框的显示数据

        :param msg: 要输出到框体的数据
        :return: None
        """
        main_window_signal.setOutPutBox.emit(msg)
        return None

    @staticmethod
    def addOne(num: int) -> int:
        """
        用于测试的函数，会输出输入数字+1的结果

        :param num: 一个数字
        :return: int
        """
        return num + 1

    @staticmethod
    def setIoInstance(instance) -> None:
        """
        设置类属性：io实例

        :param instance: io实例
        :return: None
        """
        global io_instance
        io_instance = instance
        return None

    @staticmethod
    def getIoInstance():
        """
        返回io实例

        :return: 类属性：io实例
        """
        global io_instance
        return io_instance

    @staticmethod
    def reRunTimes(times: int = 1) -> Callable:
        """
        一个装饰器，用来计算函数运行时长

        :param times: 运行次数，默认为1
        :return: 一个元组，第一项为函数的返回值，第二项为函数运行时长
        """

        def ruturnFun(fun: Callable) -> Callable:
            def runFun(*args, **kwargs) -> Tuple[Any, float]:
                _time_start = time.perf_counter()
                for _ in range(times):
                    fun_ret = fun(*args, **kwargs)
                time_used = time.perf_counter() - _time_start
                return fun_ret, time_used

            return runFun

        return ruturnFun
