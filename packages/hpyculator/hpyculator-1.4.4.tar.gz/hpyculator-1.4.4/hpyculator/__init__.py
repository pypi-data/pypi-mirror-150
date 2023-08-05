from .signal import main_window_signal
from .signal import setting_window_signal
from .main import Main

name = "hpyculator"
hpycore = Main()

STRING = (1 << 0)
NUM = (1 << 1)
FLOAT = (1 << 2)
LIST = (1 << 3)

ON = (1 << 1)
OFF = (1 << 0)  # 因为没读到就用这个作为缺省，所以每个参数的(1<<0)就是缺省

# 'output_mode'
RETURN_ONCE = (1 << 0)
RETURN_LIST = (1 << 1)
RETURN_LIST_OUTPUT_IN_ONE_LINE = (1 << 2)
NO_RETURN = (1 << 3)
NO_RETURN_SINGLE_FUNCTION = (1 << 4)