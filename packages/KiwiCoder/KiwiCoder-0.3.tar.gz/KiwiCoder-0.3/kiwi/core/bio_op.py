import asyncio
import json
import uuid
from abc import ABC, abstractmethod
from time import sleep
from typing import Dict, List, Callable

from kiwi.common.exception import ToBeImplementException, AttributeNotExistException

from kiwi.common.constant import ContainerType, PeripheryUsage

from kiwi.util.graph import DAG

from kiwi.core.bio_obj import BioObject
from .bio_entity import Container, Fluid

from .bio_periphery import Periphery
from .bio_quantity import Volume, Temperature, Time, Speed, FlowRate
from kiwi.common import SysStatus, EventName, Msg, MsgEndpoint, MsgLevel, AutoLevel, SysSignal, with_defer, defer, \
    UserMsg, watch_change, PeripheryOpException
from kiwi.util import EventBus
from .globals import Counter, InnerTimer
from ..util.encoder import CustomJSONEncoder

bus = EventBus()
counter = Counter()
inner_timer = InnerTimer()


@watch_change(watch_list=["status"])
class BioOp(ABC):
    def __init__(
            self,
            step_name: str,
            op_index: int,
            dependency_graph: DAG,
            periphery_list=None,
            auto_level=AutoLevel.FULL,
    ):
        """
        Args:
            step_name:
            op_index:
            auto_level: the operation needs human or not
            operation has at most three stages, pre run & post run can be block by human, run is the main part
        """
        self.id = None
        self.name = None
        self.step_name = step_name
        self.op_index = op_index
        self.key = BioOp.get_op_identifier(self.step_name, self.op_index)
        self.auto_level = auto_level
        self.dependency_graph = dependency_graph
        self.periphery_dict = {}  # Periphery -> List[Periphery]
        self.bio_obj_dict = Dict[int, BioObject]
        self.status = SysStatus.INIT
        self.mock = False
        self.run_funcs = List[Callable]

        bus.add_event(func=self._signal_handler,
                      event=EventName.OP_SIGNAL_RECEIVE_EVENT
                      .format(BioOp.get_op_identifier(self.step_name, self.op_index)))
        ''' handler periphery '''
        if periphery_list is not None:
            for periphery in periphery_list:
                val = self.periphery_dict.get(periphery.usage, None)
                if val is None:
                    self.periphery_dict[periphery.usage] = [periphery]
                else:
                    self.periphery_dict[periphery.usage].append(periphery)
        ''' set auto level functions '''
        if auto_level == AutoLevel.FULL:
            self.run_funcs = [self._run]
        elif auto_level == AutoLevel.SEMI:
            self.run_funcs = [self._human_run, self._run, self._human_run]
        elif auto_level == AutoLevel.HUMAN:
            self.run_funcs = [self._human_run]

    def __str__(self):
        return json.dumps(self.__dict__)

    def get_exclusive_obj_ids(self) -> []:
        exclusive_ids = []
        for _, periphery_list in self.periphery_dict.items():
            for periphery in periphery_list:
                if periphery.is_exclusive is True:
                    exclusive_ids.append(periphery.id)
        return exclusive_ids

    def delay_init(self, step_name: str, op_index: int, auto_level=AutoLevel.FULL):
        self.step_name = step_name
        self.op_index = op_index
        self.auto_level = auto_level

    def attach_periphery(self, periphery: Periphery) -> None:
        self.periphery_dict[periphery.usage].append(periphery)
        return

    def all_stage_run(self) -> SysStatus:
        """ run the whole operation, check status first """
        while self.status == SysStatus.PENDING:
            ''' sleep to yield cpu to cmd thread '''
            sleep(0.1)
        op_status = SysStatus.SUCCESS
        ''' run mock function if mock is set '''
        if self.mock:
            BioOp._print_to_screen(msg=UserMsg.OP_MOCK_START_TEMPLATE
                                   .format(self.step_name, self.op_index, "_mock"), level=MsgLevel.INFO)
            op_status = self._mock_run()
        else:
            for func in self.run_funcs:
                BioOp._print_to_screen(msg=UserMsg.OP_STAGE_START_TEMPLATE
                                       .format(self.step_name, self.op_index, func.__name__), level=MsgLevel.INFO)
                op_status = func()
        self.status = op_status
        return op_status

    @with_defer
    def _run(self) -> SysStatus:
        """ the main stage of run, execute automatically """
        op_status = SysStatus.SUCCESS
        return op_status

    def _human_run(self) -> SysStatus:
        """ notify human to operate """
        BioOp._print_to_screen(msg=UserMsg.OP_OPERATE_HUMAN_TEMPLATE.format(self.step_name, self.op_index),
                               level=MsgLevel.IMPORTANT)
        self.status = SysStatus.PENDING
        while self.status == SysStatus.PENDING:
            ''' sleep to yield cpu to cmd thread '''
            sleep(0.1)
        return SysStatus.SUCCESS

    @with_defer
    def _mock_run(self) -> SysStatus:
        """ mock the operation """
        op_status = SysStatus.SUCCESS
        return op_status

    def frame_start(self):
        """ call before update """
        self.status = SysStatus.RUNNING

    def frame_end(self):
        """ call after all update """
        self.status = SysStatus.SUCCESS

    def frame_update(self) -> bool:
        """ update operation run func per frame in validation mode """
        return False

    def _signal_handler(self, signal: SysSignal) -> None:
        if signal == SysSignal.RUN:
            self.status = SysStatus.RUNNING
            self.all_stage_run()
        elif signal == SysSignal.CONTINUE:
            self.status = SysStatus.RUNNING
        elif signal == SysSignal.SUSPEND:
            self.status = SysStatus.PENDING
        BioOp._print_to_screen(msg=UserMsg.OP_SIGNAL_TEMPLATE
                               .format(self.step_name, self.op_index, signal.name), level=MsgLevel.INFO)

    @staticmethod
    def _print_to_screen(msg: str, level: MsgLevel):
        bus.emit(event=EventName.SCREEN_PRINT_EVENT,
                 msg=Msg(msg=msg, source=MsgEndpoint.OP, destinations=[MsgEndpoint.USER_TERMINAL],
                         code=SysStatus.SUCCESS, level=level))

    def _watch(self, name, old_value, value) -> None:
        """ _watch will be called when attributes in @watch_change changes """
        dump_dict = {"id": self.id, "name": self.name, "step_name": self.step_name, "op_index": self.op_index,
                     "key": self.key, "auto_level": self.auto_level, "status": self.status}
        raw_msg = json.dumps(dump_dict, cls=CustomJSONEncoder)
        bus.emit(event=EventName.WATCH_EVENT, src=MsgEndpoint.OP, raw_msg=raw_msg)

    @staticmethod
    def get_op_identifier(step_name: str, op_index: int) -> str:
        return "sn:" + step_name + ",op:" + str(op_index)

    @abstractmethod
    def get_html_text(self) -> str:
        """ output the text describe the operation """
        pass


# ==================================== #
#      1. Writing a new protocol       #
# ==================================== #


class StartProtocolOp(BioOp):
    def __init__(self, protocol_name: str, step_name: str, op_index: int, dependency_graph: DAG):
        super().__init__(step_name, op_index, dependency_graph)
        self.protocol_name = protocol_name

    def _run(self) -> SysStatus:
        BioOp._print_to_screen(msg=UserMsg.OP_PROTOCOL_START_TEMPLATE.format(self.protocol_name),
                               level=MsgLevel.IMPORTANT)
        op_status = SysStatus.SUCCESS
        return op_status

    def get_html_text(self) -> str:
        return "<h1 style=\"font-size = 25px;\">{}</h1>".format(self.protocol_name)


class EndProtocolOp(BioOp):
    def __init__(self, step_name: str, op_index: int, dependency_graph: DAG):
        super().__init__(step_name, op_index, dependency_graph)

    def _run(self) -> SysStatus:
        BioOp._print_to_screen(msg=UserMsg.OP_PROTOCOL_END_TEMPLATE, level=MsgLevel.IMPORTANT)
        op_status = SysStatus.SUCCESS
        return op_status

    def get_html_text(self) -> str:
        return "</li></p></ol>"


class CommentOp(BioOp):
    def __init__(self, content: str, step_name: str, op_index: int, dependency_graph: DAG):
        super().__init__(step_name, op_index, dependency_graph)
        self.content = content

    def get_html_text(self) -> str:
        return "<font color = \"#800517\"><i>{}</i></font><br>".format(self.content)


class DoNothingOp(BioOp):
    """ Do nothing and wait until receive signal """

    def __init__(self, step_name: str, op_index: int, dependency_graph: DAG):
        super().__init__(step_name, op_index, dependency_graph, auto_level=AutoLevel.HUMAN)

    def _run(self) -> SysStatus:
        return self._human_run()

    def get_html_text(self) -> str:
        return ""


class DirectCallOp(BioOp):
    """ direct call core method from wrapper """

    def __init__(self, var, method_name: str, kv_args: {}, step_name: str, op_index: int, dependency_graph: DAG):
        super().__init__(step_name, op_index, dependency_graph)
        self.var = var
        self.method_name = method_name
        self.kv_args = kv_args

    def _run(self) -> SysStatus:
        func = getattr(self.var, self.method_name)
        if func is None:
            raise AttributeNotExistException("{}.{}".format(type(self.var), self.name))
        func(**self.kv_args)
        return SysStatus.SUCCESS

    def get_html_text(self) -> str:
        return ""


# ==================================== #
#      3. Measuring out materials      #
# ==================================== #


class MeasureFluidOp(BioOp):
    def __init__(self, fluid: Fluid, container: Container, vol: Volume, step_name: str, op_index: int,
                 dependency_graph: DAG, periphery_list=None, auto_level=AutoLevel.FULL):
        super().__init__(step_name, op_index, dependency_graph, periphery_list, auto_level)
        self.fluid = fluid
        self.container = container
        self.vol = vol
        ''' simulation variable '''
        self.accumulate_vol = Volume(0, "ml")
        ''' dependency config '''
        measured_fluid = Fluid("measure fluid")
        dependency_graph.add_node(measured_fluid)
        dependency_graph.add_node(fluid)
        dependency_graph.add_edge(fluid, measured_fluid)
        if container.content is None:
            dependency_graph.add_node(container)
            dependency_graph.add_edge(measured_fluid, container)
        else:
            dependency_graph.add_node(container.content)
            dependency_graph.add_edge(measured_fluid, container.content)

    @with_defer
    def _run(self) -> SysStatus:
        defer(lambda: BioOp._print_to_screen(msg=UserMsg.OP_STAGE_END_TEMPLATE
                                             .format(self.step_name, self.op_index, "_run"),
                                             level=MsgLevel.INFO))
        """ open container if necessary"""
        self.fluid.open_all()
        self.container.open_all()
        """ search for drivers, and stop drivers until read threshold value """
        drivers = self.periphery_dict[PeripheryUsage.DRIVER]
        measure_instrums = self.periphery_dict[PeripheryUsage.MEASURE]
        if len(drivers) == 0 or len(measure_instrums) != 1:
            raise PeripheryOpException(self.name)
        for driver in drivers:
            driver.start()
        result_value = measure_instrums[0].accumulate_read(self.vol.value, 3600)
        BioOp._print_to_screen(msg="Measure fluid {}".format(result_value), level=MsgLevel.GOSSIP)
        for driver in drivers:
            driver.shutdown()
        """ close container if necessary"""
        self.fluid.close_all()
        self.container.close_all()
        op_status = SysStatus.SUCCESS
        return op_status

    def frame_start(self):
        self.accumulate_vol = Volume(0, "ml")
        self.status = SysStatus.RUNNING

    def frame_end(self):
        self.status = SysStatus.SUCCESS

    def frame_update(self) -> bool:
        drivers = self.periphery_dict[PeripheryUsage.DRIVER]
        sum_flow_rate = FlowRate(0, "ml/s")
        for driver in drivers:
            sum_flow_rate = sum_flow_rate + driver.flow_rate
        delta_vol = sum_flow_rate * Time(inner_timer.delta_time, "s")
        self.accumulate_vol = self.accumulate_vol + delta_vol
        self.container.cur_volume = self.container.cur_volume + delta_vol
        if self.accumulate_vol > self.vol:
            return False
        return True

    def get_html_text(self) -> str:
        """ output the text describe the operation """
        text_str = "Measure out "
        if self.vol is not None:
            text_str += self.vol.text() + " of "
        text_str += "<font color=#357EC7>{}</font> into {}.<br>" \
            .format(self.fluid.name, self.container.name)
        return text_str


# ==================================== #
#        4. Combination/mixing         #
# ==================================== #

def _mix_graph_construct(container: Container, dependency_graph: DAG):
    mix_fluid = Fluid("mix")
    dependency_graph.add_node(mix_fluid)
    prev_content = container.content
    container.content = Container(container_type=ContainerType.FAKE_CONTAINER)
    container.content.name = "container with contents mixed"
    container.content.key = str(uuid.uuid4().hex)
    dependency_graph.add_node(container.content)
    if prev_content is not None:
        dependency_graph.add_edge(prev_content, mix_fluid)
    else:
        dependency_graph.add_edge(container, mix_fluid)
    dependency_graph.add_edge(mix_fluid, container.content)


class VortexOp(BioOp):
    def __init__(self, container: Container, step_name: str, op_index: int, dependency_graph: DAG,
                 periphery_list=None, auto_level=AutoLevel.FULL):
        super().__init__(step_name, op_index, dependency_graph, periphery_list, auto_level)
        ''' dependency config '''
        _mix_graph_construct(container, self.dependency_graph)

    def _run(self) -> SysStatus:
        print("run vortex op, hello world")
        op_status = SysStatus.SUCCESS
        return op_status

    def get_html_text(self) -> str:
        """ output the text describe the operation """
        return "Vortex the mixture for a few secs.<br>"


class TapOp(BioOp):
    def __init__(self, container: Container, step_name: str, op_index: int, dependency_graph: DAG,
                 periphery_list=None, auto_level=AutoLevel.FULL):
        super().__init__(step_name, op_index, dependency_graph, periphery_list, auto_level)
        ''' dependency config '''
        _mix_graph_construct(container, self.dependency_graph)

    def _run(self) -> SysStatus:
        print("run tap op, hello world")
        op_status = SysStatus.SUCCESS
        return op_status

    def get_html_text(self) -> str:
        """ output the text describe the operation """
        return "Gently tap the mixture for a few secs.<br>"


class DissolveOp(BioOp):
    def __init__(self, container: Container, step_name: str, op_index: int, dependency_graph: DAG,
                 periphery_list=None, auto_level=AutoLevel.FULL):
        super().__init__(step_name, op_index, dependency_graph, periphery_list, auto_level)
        _mix_graph_construct(container, self.dependency_graph)

    def _run(self) -> SysStatus:
        print("run dissolve op, hello world")
        op_status = SysStatus.SUCCESS
        return op_status

    def get_html_text(self) -> str:
        """ output the text describe the operation """
        return "Dissolve the pellet in the solution.<br>"


# ==================================== #
#              6. Storage              #
# ==================================== #

class WaitOp(BioOp):
    """ Holds the given container for the specified unit of time. """

    def __init__(self, container: Container, wait_time: Time, step_name: str, op_index: int, dependency_graph: DAG,
                 periphery_list=None, auto_level=AutoLevel.FULL):
        super().__init__(step_name, op_index, dependency_graph, periphery_list, auto_level)
        self.container = container
        self.wait_time = wait_time
        ''' dependency config '''
        fluid = Fluid("wait")
        self.dependency_graph.add_node(fluid)
        self.dependency_graph.add_node(container)
        container.content = Container(container_type=ContainerType.FAKE_CONTAINER)
        container.content.name = "container with contents after waiting"
        self.dependency_graph.add_edge(fluid, container.content)
        self.dependency_graph.add_edge(container, fluid)

    def frame_start(self):
        self.status = SysStatus.RUNNING

    def frame_end(self):
        self.status = SysStatus.SUCCESS

    def frame_update(self) -> bool:
        return False

    def _run(self) -> SysStatus:
        defer(lambda: BioOp._print_to_screen(msg=UserMsg.OP_STAGE_END_TEMPLATE
                                             .format(self.step_name, self.op_index, "_run"),
                                             level=MsgLevel.INFO))
        op_status = SysStatus.SUCCESS
        wait_seconds = self.wait_time.std_value()
        sleep(wait_seconds)
        return op_status

    def get_html_text(self) -> str:
        return "Keep {} aside for {}{}.<br>".format(self.container.name, self.wait_time.value,
                                                    self.wait_time.unit_denote)


class StoreOp(BioOp):
    """ Stores the specified container at a given temperature. """

    def __init__(self, container: Container, temp: Temperature, step_name: str, op_index: int, dependency_graph: DAG,
                 periphery_list=None, auto_level=AutoLevel.FULL):
        super().__init__(step_name, op_index, dependency_graph, periphery_list, auto_level)
        self.container = container
        self.temp = temp
        ''' dependency config '''
        fluid = Fluid("store")
        self.dependency_graph.add_node(fluid)
        self.dependency_graph.add_node(container)
        self.dependency_graph.add_edge(container, fluid)
        container.content = Container(container_type=ContainerType.FAKE_CONTAINER)
        container.content.name = "container stored at required temperature"
        self.dependency_graph.add_node(container.content)
        self.dependency_graph.add_edge(fluid, container.content)

    def frame_start(self):
        self.status = SysStatus.RUNNING

    def frame_end(self):
        self.status = SysStatus.SUCCESS

    def frame_update(self) -> bool:
        return False

    def _run(self) -> SysStatus:
        print("run store op, hello world")
        op_status = SysStatus.SUCCESS
        return op_status

    def get_html_text(self) -> str:
        """ output the text describe the operation """
        return "Store {} at {}C.".format(self.container.name, self.temp.value)


# ==================================== #
#           7. Centrifugation          #
# ==================================== #

class CentrifugePelletOp(BioOp):
    """ Performs centrifugation of given container at the specified temperature, speed and time and yields a pellet.
    The supernatant is discarded. """

    def __init__(self, container: Container, speed: Speed, temp: Temperature, time: Time, step_name: str, op_index: int,
                 dependency_graph: DAG, periphery_list=None, auto_level=AutoLevel.FULL):
        super().__init__(step_name, op_index, dependency_graph, periphery_list, auto_level)
        self.container = container
        self.speed = speed
        self.temp = temp
        self.time = time
        ''' dependency config '''
        fluid = Fluid("centrifuge pellet")
        self.dependency_graph.add_node(fluid)
        self.dependency_graph.add_node(container.content)
        self.dependency_graph.add_edge(container.content, fluid)
        container.content = Container(container_type=ContainerType.FAKE_CONTAINER)
        container.content.name = "container with pellet"
        self.dependency_graph.add_node(container.content)
        self.dependency_graph.add_edge(fluid, container.content)

    def _run(self) -> SysStatus:
        print("run centrifuge pellet op, hello world")
        op_status = SysStatus.SUCCESS
        return op_status

    def get_html_text(self) -> str:
        """ output the text describe the operation """
        text_str = "Centrifuge " + self.container.name + " at " + self.speed.text() + " for " + self.time.text() \
                   + "at <b><font color=#357EC7>{}</font></b>, gently aspirate out the supernatant and discard it.<br>" \
                       .format(self.temp.text())
        return text_str


# ==================================== #
#   9. Transfer of fluid and columns   #
# ==================================== #

class TransferOp(BioOp):
    def __init__(self, from_container: Container, to_container: Container, step_name: str, op_index: int,
                 dependency_graph: DAG, periphery_list=None, auto_level=AutoLevel.FULL):
        super().__init__(step_name, op_index, dependency_graph, periphery_list, auto_level)
        self.from_container = from_container
        self.to_container = to_container
        ''' dependency config '''
        fluid = Fluid("transfer")
        self.dependency_graph.add_node(fluid)
        if from_container.content is not None:
            self.dependency_graph.add_node(from_container.content)
            self.dependency_graph.add_edge(from_container.content, fluid)
        else:
            self.dependency_graph.add_node(from_container)
            self.dependency_graph.add_edge(from_container, fluid)
        if to_container.content is not None:
            self.dependency_graph.add_node(to_container.content)
            self.dependency_graph.add_edge(fluid, to_container.content)
        else:
            self.dependency_graph.add_node(to_container)
            self.dependency_graph.add_edge(fluid, to_container)

    def frame_start(self):
        self.status = SysStatus.RUNNING

    def frame_end(self):
        self.status = SysStatus.SUCCESS

    def frame_update(self) -> bool:
        return False

    def _run(self) -> SysStatus:
        defer(lambda: BioOp._print_to_screen(msg=UserMsg.OP_STAGE_END_TEMPLATE
                                             .format(self.step_name, self.op_index, "_run"),
                                             level=MsgLevel.INFO))
        op_status = SysStatus.SUCCESS
        """ open container """
        self.from_container.open_all()
        """ transfer all """

        """ open container """
        self.to_container.close_all()
        return op_status

    def get_html_text(self) -> str:
        text_str = "Transfer {} into {}.<br>".format(self.from_container.name, self.to_container.name)
        return text_str
