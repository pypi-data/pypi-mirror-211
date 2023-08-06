import json
import math
from abc import abstractmethod

from kiwi.common import NotSupportUnit
from kiwi.core.bio_obj import BioObject


class Quantity(BioObject):
    def __init__(self, value: float, unit_denote: str):
        super().__init__()
        self.value = value
        self.unit_denote = unit_denote

    @abstractmethod
    def std_value(self) -> float:
        """ return value in common unit in bio experiments """
        pass

    def text(self) -> str:
        return "{}{}".format(self.value, self.unit_denote)

    def __eq__(self, other):
        is_equal = math.isclose(self.std_value(), other.std_value(), rel_tol=1e-5)
        return is_equal

    def __ne__(self, other):
        is_equal = math.isclose(self.std_value(), other.std_value(), rel_tol=1e-5)
        return not is_equal

    def __lt__(self, other):
        return self.std_value() < other.std_value()

    def __le__(self, other):
        return self.std_value() <= other.std_value()

    def __gt__(self, other):
        return self.std_value() > other.std_value()

    def __ge__(self, other):
        return self.std_value() >= other.std_value()

    def obj2dict(self):
        obj_dict = {"value": self.value, "unit": self.unit_denote}
        return obj_dict

    def __str__(self):
        return json.dumps(self.obj2dict())


class Volume(Quantity):
    std_unit = "ml"
    max_val = 1e5

    def __init__(self, value: float, unit_denote: str):
        super().__init__(value, unit_denote)

    def std_value(self) -> float:
        if self.unit_denote == "ml":
            return self.value
        elif self.unit_denote == "ul":
            return self.value * 0.001

    def __add__(self, other):
        value = self.std_value() + other.std_value()
        return Volume(value, Volume.std_unit)

    def __sub__(self, other):
        value = self.std_value() - other.std_value()
        return Volume(value, Volume.std_unit)

    def __mul__(self, other):
        """ multiple a float """
        value = self.std_value() * other
        return Volume(value, Volume.std_unit)


class Speed(Quantity):
    def __init__(self, value: float, unit_denote: str):
        super().__init__(value, unit_denote)

    def std_value(self) -> float:
        return self.value


class Temperature(Quantity):
    ON_ICE = 0
    ON_BOIL = 100
    ROOM = 28

    def __init__(self, temp: float):
        super().__init__(value=temp, unit_denote="dc")
        self.temp = temp

    def std_value(self) -> float:
        return self.temp


class Time(Quantity):
    std_unit = "s"

    def __init__(self, value: float, unit_denote: str):
        super().__init__(value, unit_denote)

    def std_value(self) -> float:
        return self.value


class FlowRate(Quantity):
    std_unit = "ml/s"

    def __init__(self, value: float, unit_denote: str):
        super().__init__(value, unit_denote)

    def std_value(self) -> float:
        return self.value

    def __add__(self, other):
        value = self.std_value() + other.std_value()
        return FlowRate(value, FlowRate.std_unit)

    def __mul__(self, other):
        """ multiple a Time, return volume """
        if not isinstance(other, Time):
            raise NotSupportUnit("Time")
        value = self.std_value() * other.std_value()
        return Volume(value, Volume.std_unit)
