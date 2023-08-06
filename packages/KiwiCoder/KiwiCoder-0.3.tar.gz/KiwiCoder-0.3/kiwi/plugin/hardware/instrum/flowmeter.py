import struct

import serial

from kiwi.core import MeasureInstrumPeriphery
from kiwi.common import class_mock_enable, PeripheryUsage
from typing import Optional

read_transient_flow_cmd = [0x01, 0x03, 0x00, 0x10, 0x00, 0x02, 0xC5, 0xCE]
read_total_flow_cmd = [0x01, 0x03, 0x00, 0x1A, 0x00, 0x02, 0xE5, 0xCC]
set_digital_control_cmd = [0x01, 0x10, 0x00, 0x74, 0x00, 0x02, 0x04, 0x00, 0x00, 0x41, 0xD0, 0xC4, 0xB4]
set_analog_control_cmd = [0x01, 0x10, 0x00, 0x74, 0x00, 0x02, 0x04, 0x00, 0x00, 0x41, 0xCB, 0xC4, 0xBE]

read_interval = 1


@class_mock_enable
class FlowMeter(MeasureInstrumPeriphery):
    def __init__(self, port: str, name="", usage=PeripheryUsage.BASE, mock=False, mock_obj=None):
        super().__init__(name=name, usage=usage, mock=mock, mock_obj=mock_obj)
        self.port = port
        self.ser = None

    def prepare(self):
        self.ser = serial.Serial(port=self.port,
                                 baudrate=115200,
                                 timeout=1,
                                 inter_byte_timeout=0.01,
                                 exclusive=True)
    def __mock_prepare__(self):
        pass

    def read(self) -> Optional[float]:
        try:
            val_result = self.read_value(read_total_flow_cmd)
        except Exception as e:
            print(e)
            return None
        return val_result

    def read_value(self, cmd: list[int]):
        self.ser.write(cmd)
        line = self.ser.read(9)
        val_buf = line[3:7]
        val_bytes = bytearray([val_buf[1], val_buf[0], val_buf[3], val_buf[2]])
        val = struct.unpack('<f', val_bytes)[0]
        return val

    def __mock_read__(self) -> Optional[float]:
        print("\nfm mock read")
        return 10000.0

    def start(self):
        pass

    def shutdown(self):
        pass
