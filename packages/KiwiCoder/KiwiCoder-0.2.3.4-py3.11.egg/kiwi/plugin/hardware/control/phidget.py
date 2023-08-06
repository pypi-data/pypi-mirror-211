from Phidget22.Devices.DigitalOutput import DigitalOutput

from kiwi.common import PeripheryUsage
from kiwi.common.common import class_mock_enable

from kiwi.core import ControlPeriphery

from threading import Timer, Lock


class PhidgetRelayPort(object):
    def __init__(self, vintport, channel, hold_duty=1.0, hit_delay=0.2):
        self.vintport = vintport
        self.channel = channel
        self.hold_duty = hold_duty
        self.hit_delay = hit_delay
        self.rly = None
        self.lock = None
        self.state = None
        self.t = None

    def prepare(self):
        self.rly = DigitalOutput()
        self.rly.setHubPort(self.vintport)
        self.rly.setChannel(self.channel)
        self.rly.openWaitForAttachment(5000)
        self.lock = Lock()
        self.state = False  # false -> closed, true->open, or duty>0%
        self.hit_delay = self.hit_delay
        self.hold_duty = self.hold_duty
        self.t = Timer(0, None)

    def open(self):
        def _hold():
            with self.lock:
                # double check it hasn't been closed in the mean time!
                if self.state == True:
                    self.rly.setDutyCycle(self.hold_duty)

        with self.lock:
            self.rly.setDutyCycle(1.0)
            self.state = True

        # set hold_duty after hit_delay seconds
        self.t = Timer(self.hit_delay, _hold)
        self.t.start()

    def close(self):
        with self.lock:
            self.t.cancel()
            self.rly.setDutyCycle(0.0)
            self.rly.state = False

    def start(self):
        pass

    def shutdown(self):
        pass


@class_mock_enable
class PhidgetRelay(ControlPeriphery):
    def __init__(self, vintport, nvalves=16, name="", usage=PeripheryUsage.BASE, mock=False, mock_obj=None):
        super().__init__(name=name, usage=usage, mock=mock, mock_obj=mock_obj)
        self.vintport = vintport
        self.nvalves = nvalves
        self.relays = []
        self.gen_port_idx = 0
        self.id2port = {}

    def register(self, bio_id: int, port: int) -> None:
        self.id2port[bio_id] = port

    def prepare(self):
        for ch in range(self.nvalves):
            _rly = PhidgetRelayPort(self.vintport, ch, hold_duty=1.0)
            self.relays.append(_rly)

        for relay in self.relays:
            relay.prepare()

    def __mock_prepare__(self):
        pass

    def start(self):
        pass

    def shutdown(self):
        pass

    def set_signal(self, bio_id: int):
        port_id = self.id2port[bio_id]
        relay = self.relays[port_id]
        relay.open()

    def unset_signal(self, bio_id: int):
        port_id = self.id2port[bio_id]
        relay = self.relays[port_id]
        relay.close()

    def set_signal_with_value(self, bio_id: int, val: float):
        pass

    def __mock_set_signal__(self, bio_id: int):
        pass

    def __mock_unset_signal__(self, bio_id: int):
        pass
