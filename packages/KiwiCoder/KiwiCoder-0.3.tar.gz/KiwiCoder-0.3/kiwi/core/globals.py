from queue import Queue

from kiwi.common import singleton


@singleton
class SysVar:
    var_map = {
        "FPS": 50,
        "CUR_FPS": -1.0,
    }


@singleton
class Counter:
    def __init__(self):
        self.cnt = 0

    def get_new_id(self) -> int:
        ret = self.cnt
        self.cnt += 1
        return ret


@singleton
class InnerTimer:
    def __init__(self):
        self.sys_var_ref = SysVar()

    @property
    def delta_time(self) -> float:
        fps = self.sys_var_ref.var_map['FPS']
        return 1.0/fps





