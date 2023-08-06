import json
import uuid

from enum import Enum

from kiwi.common import watch_change, AttributeNotExistException
from kiwi.core.globals import Counter
from kiwi.util.encoder import CustomJSONEncoder
from kiwi.util.event import EventBus

from kiwi.common.constant import SysStatus, MsgEndpoint, EventName, MathOp, MsgLevel

bus = EventBus()
counter = Counter()


class BioType(Enum):
    DEFAULT = 0
    Periphery = 1


@watch_change(watch_list=["status"])
class BioObject(object):
    """
    class member end with _um means the function can not be mocked
    """

    def __init__(self, name="", mock=False, mock_obj=None, is_exclusive=True, periphery_list=None):
        self.id = counter.get_new_id()
        self.key = None
        self.name = name
        self.mock = mock
        self.mock_obj = mock_obj
        self.is_exclusive = is_exclusive
        self.status = SysStatus.INIT
        self.content = None
        self.periphery_dict = {}  # Periphery -> List[Periphery]
        ''' handler periphery '''
        if periphery_list is not None:
            for periphery in periphery_list:
                val = self.periphery_dict.get(periphery.usage, None)
                if val is None:
                    self.periphery_dict[periphery.usage] = [periphery]
                else:
                    self.periphery_dict[periphery.usage].append(periphery)

    def set_id(self, obj_id: int) -> None:
        self.id = obj_id

    def get_id_um(self) -> int:
        return self.id

    def get_bio_type_um(self) -> BioType:
        return self.bio_type

    def is_mock_um(self) -> bool:
        return self.mock

    def set_mock_um(self, is_mock: bool) -> None:
        self.mock = is_mock

    def add_watch_attribute(self, watch_attr: str) -> None:
        # target_attr = getattr(self, watch_attr, None)
        # if target_attr is None:
        #     raise AttributeNotExistException(watch_attr)
        self.watch_set.add(watch_attr)
        print(self.watch_set)

    def add_alarm_attribute(self, alarm_attr: str, math_op: MathOp, threshold_value) -> None:
        # target_attr = getattr(self, alarm_attr, None)
        # if target_attr is None:
        #     raise AttributeNotExistException(alarm_attr)
        self.alarm_dict[alarm_attr] = (math_op, threshold_value)
        print(self.alarm_dict)

    def update(self):
        """ update bio object per frame in mock mode """
        pass

    def _watch(self, name, old_value, value) -> None:
        """ _watch will be called when attributes in @watch_change changes"""
        # print("call watch-------")
        msg_dict = dict()
        msg_dict["obj"] = self.obj2dict()
        msg_dict["watch"] = {"name": name, "old_value": str(old_value), "value": str(value)}
        raw_msg = json.dumps(msg_dict, cls=CustomJSONEncoder)
        bus.emit(event=EventName.WATCH_EVENT, src=MsgEndpoint.BIO_OBJ, raw_msg=raw_msg)

    def _alarm(self, name, value, threshold_value, math_op) -> None:
        # print("call alarm-------")
        msg_dict = dict()
        msg_dict["obj"] = self.obj2dict()
        msg_dict["alarm"] = {"name": name, "value": str(value), "threshold_value": str(threshold_value),
                             "math_op": math_op}
        raw_msg = json.dumps(msg_dict, cls=CustomJSONEncoder)
        bus.emit(event=EventName.WATCH_EVENT, src=MsgEndpoint.BIO_OBJ, raw_msg=raw_msg, level=MsgLevel.WARN)

    def obj2dict(self):
        obj_dict = {"id": self.id, "key": self.key, "name": self.name, "mock": self.mock, "status": self.status}
        return obj_dict

    def __str__(self):
        return json.dumps(self.obj2dict())


class FakeBioObject(BioObject):
    """ fake bio object is used in dependency graph """
    def __init__(self, name="", mock=False, mock_obj=None, periphery_list=None):
        super().__init__(name, mock, mock_obj, periphery_list)


