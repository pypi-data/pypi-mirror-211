from kiwi.common import class_mock_enable, PeripheryUsage
from kiwi.core import SignalPeriphery, ControlPeriphery


@class_mock_enable
class Valve(SignalPeriphery):
    def __init__(self, control_periphery: ControlPeriphery, port: int, name="", usage=PeripheryUsage.BASE, mock=False, mock_obj=None):
        super().__init__(control_periphery=control_periphery, port=port, name=name, usage=usage, mock=mock, mock_obj=mock_obj)

    def prepare(self):
        self.attach_to.register(self.id, self.port)

    def start(self):
        self.attach_to.set_signal(self.id)
        print("valve port {} start, id {}".format(self.port, self.id))

    def shutdown(self):
        self.attach_to.unset_signal(self.id)
        print("valve port {} shutdown, id {}".format(self.port, self.id))


