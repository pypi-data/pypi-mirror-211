from abc import abstractmethod
from typing import Optional
from time import sleep

from kiwi.core.bio_obj import BioObject
from kiwi.common import PeripheryUsage


class Periphery(BioObject):
    def __init__(self, name: str, usage: PeripheryUsage, mock=False, mock_obj=None):
        super().__init__(name=name, mock=mock, mock_obj=mock_obj)
        self.usage = usage

    @abstractmethod
    def prepare(self):
        """ prepare the running env for periphery and initialize """
        pass

    @abstractmethod
    def start(self):
        """ start the periphery """
        pass

    @abstractmethod
    def shutdown(self):
        """ shutdown the periphery """
        pass


# ==================================== #
#        Periphery type                #
# ==================================== #

class ControlPeriphery(Periphery):
    """ center hardware that controls other periphery, e.g. Raspberry Pi"""

    def __init__(self, name="", usage=PeripheryUsage.BASE, mock=False, mock_obj=None):
        super().__init__(name=name, usage=usage, mock=mock, mock_obj=mock_obj)

    @abstractmethod
    def register(self, bio_id: int, port: int) -> None:
        pass

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass

    @abstractmethod
    def set_signal(self, bio_id: int):
        """ set signal with default or max value to the port """
        pass

    @abstractmethod
    def unset_signal(self, bio_id: int):
        pass

    @abstractmethod
    def set_signal_with_value(self, bio_id: int, val: float):
        pass


class InstrumPeriphery(Periphery):
    """ bio instruments, e.g. PCR """

    def __init__(self, name="", usage=PeripheryUsage.BASE, mock=False, mock_obj=None):
        super().__init__(name=name, usage=usage, mock=mock, mock_obj=mock_obj)

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass


class SignalPeriphery(Periphery):
    """
    a periphery is commonly controlled by a attach_to periphery
    """

    def __init__(self, control_periphery: ControlPeriphery, port: int, name="", usage=PeripheryUsage.BASE, mock=False, mock_obj=None):
        self.attach_to = control_periphery
        self.port = port
        super().__init__(name=name, usage=usage, mock=mock, mock_obj=mock_obj)

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass


# ==================================== #
#        Specific instrum              #
# ==================================== #

class MeasureInstrumPeriphery(InstrumPeriphery):
    def __init__(self, name="", usage=PeripheryUsage.BASE, mock=False, mock_obj=None):
        super().__init__(name=name, usage=usage, mock=mock, mock_obj=mock_obj)

    def prepare(self):
        pass

    def start(self):
        pass

    def shutdown(self):
        pass

    def read(self) -> Optional[float]:
        print("should not be called")
        pass

    def accumulate_read(self, target: float, times_in_second: int, interval: float = 0.1) -> Optional[float]:
        accumulate = 0.0
        last_measured = self.read()
        print("threshold:{}".format(target))
        while accumulate < target:
            measured = self.read()
            if measured is None:
                print("read is None")
                continue
            measure_delta = ((last_measured + measured) / 2) * interval / times_in_second
            accumulate += measure_delta
            last_measured = measured
            sleep(interval)
            # print("accum:{}".format(accumulate))
        return accumulate
