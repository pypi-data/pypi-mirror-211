import json
import uuid

from .bio_obj import BioObject
from kiwi.common import ContainerType, watch_change, MathOp
from .bio_quantity import Temperature, Volume


@watch_change(watch_list=["cur_volume"], alarm_list=[("volume", MathOp.LE, Volume(0, "ml"))])
class Container(BioObject):
    def __init__(self, container_type: ContainerType, name="", fluid=None,
                 volume=Volume(Volume.max_val, "ml"), sample_io_peripheries=None):
        """
        Args:
            container_type:
            name:
            fluid:
            volume:
            sample_io_peripheries: containers has holes for fluids to float in and float out. Switches are controlled by signal peripheries
        """
        super().__init__(name=name)
        if sample_io_peripheries is None:
            sample_io_peripheries = list()
        self.key = str(uuid.uuid4().hex)
        self.volume = volume
        self.cur_volume = volume
        self.sample_io_peripheries = sample_io_peripheries

    def open(self, hole_id):
        self.sample_io_peripheries[hole_id].start()

    def close(self, hole_id):
        self.sample_io_peripheries[hole_id].shutdown()

    def open_all(self):
        for periphery in self.sample_io_peripheries:
            periphery.start()

    def close_all(self):
        for periphery in self.sample_io_peripheries:
            periphery.shutdown()






class Column(Container):
    pass


class Slide(Container):
    pass


class Fluid(BioObject):
    def __init__(self, name: str, state=None, temp=Temperature.ROOM, volume=Volume(100, "ml"), sample_io_peripheries=None):
        super().__init__(name=name)
        self.key = str(uuid.uuid4().hex)
        self.temp = temp
        self.volume = volume
        self.sample_io_peripheries = sample_io_peripheries

    def open(self, hole_id):
        self.sample_io_peripheries[hole_id].start()

    def close(self, hole_id):
        self.sample_io_peripheries[hole_id].shutdown()

    def open_all(self):
        for periphery in self.sample_io_peripheries:
            periphery.start()

    def close_all(self):
        for periphery in self.sample_io_peripheries:
            periphery.shutdown()


class Solid(Fluid):
    pass


class Plate(Solid):
    pass


class Tissue(Solid):
    pass
