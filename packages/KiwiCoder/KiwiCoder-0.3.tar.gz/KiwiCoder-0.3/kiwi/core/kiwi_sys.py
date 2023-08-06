import asyncio
import datetime
import inspect
import re
import sys
import uuid
import time

from kiwi.wrapper.wrapper import Wrapper, wrapper_raw_t

from kiwi.core.step import Step
from kiwi.endpoint.server import WebSocket, KiwiHttpServer

from kiwi.core.report import ReportGen
from kiwi.util.graph import DAG

from kiwi.core.bio_obj import BioObject
from typing import Dict, Callable
from kiwi.core.sched import StepController
from kiwi.core.globals import Counter, SysVar
from kiwi.common import singleton, ConstWrapper, ScheduleMode, ModuleNotFoundException, ClassNotFoundException, Config, \
    SysStatus, MsgLevel, MsgEndpoint, EventName, Msg, UserMsg, UserDefined, BioObjNotExistException, PlaceHolder
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from kiwi.util import EventBus

bus = EventBus()
counter = Counter()


@singleton
class ProtocolGeneric:
    """GenericEnv class handles user defined wrapper, and makes a basic environment for protocol """

    def __init__(self):
        self.protocol_name = None
        self.wrappers = []
        self.root_step = Step(name="root_step", step_name="0", wait_list=[], children_parallel_list=[], repeat_times=1)
        self.steps_generic = []
        self.steps_generic.append(self.root_step)
        self.fluid_generic = []
        self.periphery_generic = []
        self.container_generic = []
        self.id_core_map = dict()
        self.dependency_graph_generic = DAG()
        self.overload_core_obj = set()
        ''' config '''
        self.watch_list = []
        self.alarm_list = []
        self.mock_bio_obj_map = {}
        self.mock_op_map = {}

    def add_overload_obj(self, overload_name: str) -> None:
        self.overload_core_obj.add(overload_name)

    def append_wrapper(self, wrapper):
        self.wrappers.append(wrapper)
        """ build core from wrapper """
        self._wrapper2core(*wrapper.args, **wrapper.kwargs, wrapper=wrapper)

    def build_wrapper(self):
        """ build configure and connect to core """
        self._build_monitor()
        self._build_mock()

    def _build_monitor(self):
        """ attach monitor after core is built """
        watch_list = self.watch_list
        alarm_list = self.alarm_list
        for watch_raw in watch_list:
            bio_obj_name = watch_raw[0]
            bio_obj_attr = watch_raw[1]
            bio_obj = self._get_bio_obj_by_name(bio_obj_name)
            if bio_obj is None:
                raise BioObjNotExistException(bio_obj_name)
            bio_obj.add_watch_attribute(bio_obj_attr)
        for alarm_raw in alarm_list:
            bio_obj_name = alarm_raw[0]
            bio_obj_attr = alarm_raw[1]
            operator = alarm_raw[2]
            threshold_value = alarm_raw[3]
            bio_obj = self._get_bio_obj_by_name(bio_obj_name)
            if bio_obj is None:
                raise BioObjNotExistException(bio_obj_name)
            bio_obj.add_alarm_attribute(bio_obj_attr, operator, threshold_value)

    def _build_mock(self):
        """ set mock status after build core """
        mock_bio_obj_map = self.mock_bio_obj_map
        bio_obj_include_list = mock_bio_obj_map.get(PlaceHolder.INCLUDE, [])
        bio_obj_exclude_list = mock_bio_obj_map.get(PlaceHolder.EXCLUDE, [])
        bio_obj_exclude_set = set()
        ''' handle bio object mock '''
        for bio_obj_exclude in bio_obj_exclude_list:
            bio_obj_exclude_set.add(bio_obj_exclude)
        if len(bio_obj_include_list) == 1 and bio_obj_include_list[0] == PlaceHolder.ALL:
            bio_obj_all = self._get_all_bio_obj()
            for bio_obj in bio_obj_all:
                if bio_obj.name not in bio_obj_exclude_set:
                    bio_obj.mock = True
        else:
            for bio_obj_name in bio_obj_include_list:
                bio_obj = self._get_bio_obj_by_name(bio_obj_name)
                if bio_obj is None:
                    raise BioObjNotExistException(bio_obj_name)
                bio_obj.mock = True
        ''' handle operation mock '''
        mock_op_map = self.mock_op_map
        op_include_list = mock_op_map.get(PlaceHolder.INCLUDE, [])
        op_exclude_list = mock_op_map.get(PlaceHolder.EXCLUDE, [])
        op_exclude_set = set()
        for op_exclude in op_exclude_list:
            op_exclude_set.add(op_exclude)
        if len(op_include_list) == 1 and op_include_list[0] == PlaceHolder.ALL:
            for step in self.steps_generic:
                for op in step.operations:
                    key = op.key
                    if key not in op_exclude_set:
                        op.mock = True
        else:
            for op_key in op_include_list:
                ''' op key format like sn:1,op:0 '''
                param_list = op_key.split(',')
                step_name = param_list[0][3:]
                op_index_str = param_list[1][3:]
                op_idx = int(op_index_str)
                for step in self.steps_generic:
                    if step_name == step.step_name:
                        step.operations[op_idx].mock = True

    def _get_bio_obj_by_name(self, name):
        for bio_obj in self.fluid_generic:
            if bio_obj.name == name:
                return bio_obj
        for bio_obj in self.periphery_generic:
            if bio_obj.name == name:
                return bio_obj
        for bio_obj in self.container_generic:
            if bio_obj.name == name:
                return bio_obj
        return None

    def _get_all_bio_obj(self):
        ret = []
        ret.extend(self.fluid_generic)
        ret.extend(self.periphery_generic)
        ret.extend(self.container_generic)
        return ret

    def _wrapper2core(self, wrapper, *args, **kwargs):
        if ConstWrapper.is_op_wrapper(wrapper.get_wrapper_type()):
            self._op_wrapper2core(wrapper, *args, **kwargs)
        else:
            self._comm_wrapper2core(wrapper, *args, **kwargs)

    def _op_wrapper2core(self, wrapper, *args, **kwargs):
        """ process wrapper parameters and convert to core object """
        current_step = self.steps_generic[len(self.steps_generic) - 1]
        template_class_name = ConstWrapper.get_op_class_name(wrapper.get_wrapper_type())
        ''' mapping wrapper parameter to core '''
        process_args, process_kwargs = self._param_replace_wrapper2core(*args, **kwargs)
        ''' load user defined class or builtin class '''
        if wrapper.class_name() in self.overload_core_obj:
            target_class_template = import_dynamic(Config.USER_DEFINED_PACKAGE, template_class_name)
        else:
            target_class_template = import_dynamic(Config.CORE_OP_PACKAGE, template_class_name)
        op = target_class_template(step_name=current_step.step_name, op_index=len(current_step.operations),
                                   dependency_graph=self.dependency_graph_generic, *process_args, **process_kwargs)
        wrapper.id = op.id
        self.id_core_map[op.id] = op
        current_step.append_operation(op)

    def _comm_wrapper2core(self, wrapper, *args, **kwargs):
        """ try to find user defined op class dynamically, or use the default one """
        if wrapper.class_name() in self.overload_core_obj:
            target_class_template = import_dynamic(Config.USER_DEFINED_PACKAGE, wrapper.class_name())
        else:
            target_class_template = import_dynamic(wrapper.package_name(), wrapper.class_name())
        ''' convert wrapper to core object '''
        ''' mapping wrapper parameter to core '''
        process_args, process_kwargs = self._param_replace_wrapper2core(*args, **kwargs)
        target_class = target_class_template(*process_args, **process_kwargs)
        if issubclass(type(target_class), BioObject):
            wrapper.id = target_class.id
            target_class.key = str(uuid.uuid4().hex)
        self.id_core_map[target_class.id] = target_class
        if wrapper.get_wrapper_type() == ConstWrapper.STEP_WRAPPER:
            self.steps_generic.append(target_class)
        elif ConstWrapper.is_periphery_wrapper(wrapper.get_wrapper_type()):
            self.periphery_generic.append(target_class)
        elif ConstWrapper.is_container_wrapper(wrapper.get_wrapper_type()):
            self.container_generic.append(target_class)
        elif ConstWrapper.is_fluid_wrapper(wrapper.get_wrapper_type()):
            self.fluid_generic.append(target_class)
        ''' inject core to wrapper '''
        wrapper.inject_core_obj(target_class)

    def _param_replace_wrapper2core(self, *args, **kwargs) -> (list, list):
        process_args = []
        process_kwargs = {}

        for param in args:
            if isinstance(type(param), type) and issubclass(type(param), Wrapper):
                wrapper_id = param.get_id()
                param = self.id_core_map[wrapper_id]
            elif isinstance(param, list):
                ''' parameter is list of wrapper '''
                raw_param = []
                for item in param:
                    if isinstance(type(item), type) and issubclass(type(item), Wrapper):
                        wrapper_id = item.get_id()
                        item = self.id_core_map[wrapper_id]
                    raw_param.append(item)
                param = raw_param
            process_args.append(param)

        for name, param in kwargs.items():
            if isinstance(type(param), type) and issubclass(type(param), Wrapper):
                wrapper_id = param.get_id()
                param = self.id_core_map[wrapper_id]
            elif isinstance(param, list):
                ''' parameter is list of wrapper '''
                raw_param = []
                for item in param:
                    if isinstance(type(item), type) and issubclass(type(item), Wrapper):
                        wrapper_id = item.get_id()
                        item = self.id_core_map[wrapper_id]
                    raw_param.append(item)
                param = raw_param
            process_kwargs[name] = param

        return process_args, process_kwargs


@singleton
class KiwiSys:
    def __init__(self, thread_pool_size: int, schedule_mode=ScheduleMode.GRAPH):
        self.obj_map = Dict[int, BioObject]
        self.obj_relation = Dict[BioObject, BioObject]
        self.step_controller = StepController(schedule_mode, ProtocolGeneric().root_step)
        self.ws_server = WebSocket(Config.WS_IP, Config.WS_PORT)
        self.http_server = KiwiHttpServer(Config.HTTP_IP, Config.HTTP_PORT)
        self.report_gen = ReportGen()
        self.thread_pool = ThreadPoolExecutor(max_workers=thread_pool_size)
        self.sys_var_map = Dict[str, Callable]

    def build_sys(self):
        """ prepare the system """
        self._init_sys_var_map()

    def shutdown_sys(self):
        pass

    def task_scanner(self):
        """ convert wrapper to core, and attach configure """
        ProtocolGeneric().build_wrapper()
        self._scan_env()

    def load_module(self):
        """ load core module and user-defined functions and class """
        import_module(Config.USER_DEFINED_PACKAGE)
        kiwi_protocol = import_dynamic(Config.USER_DEFINED_PACKAGE, UserDefined.MAIN_PROTOCOL_FUNC)
        kiwi_protocol()
        self._load_wrapper_to_core()
        self._load_user_defined_package()
        self._load_monitor_config()
        self._load_mock_config()

    def run_task(self, is_validate: bool):
        """ run prepare and protocol task """
        if is_validate:
            task_thread = Thread(target=self._single_thread_run_task)
        else:
            self._run_prepare_periphery()
            """ run task """
            task_thread = Thread(target=self._thread_run_task)
        task_thread.start()

    def report_gen_graph_topology(self, filename):
        if filename == ".":
            filename = "./report/process_graph.dot"
        else:
            filename = "./report/" + filename + ".dot"
        self.report_gen.gen_graph_topology_file(filename)
        self._print_to_screen(UserMsg.REPORT_GENERATE_TEMPLATE.format(filename))

    def report_gen_html(self, filename):
        if filename == ".":
            filename = "./report/formal.html"
        else:
            filename = "./report/" + filename + ".html"
        seq_steps = self.step_controller.seq_steps()
        fluids = ProtocolGeneric().fluid_generic
        periphery_list = ProtocolGeneric().periphery_generic
        containers = ProtocolGeneric().container_generic
        self.report_gen.gen_html_report_file(filename, seq_steps, fluids, periphery_list, containers)
        self._print_to_screen(UserMsg.REPORT_GENERATE_TEMPLATE.format(filename))

    def set_sys_variable(self, var_name: str, var_value) -> str:
        self.sys_var_map[var_name + "_setter"](var_value)
        val = self.sys_var_map[var_name + "_getter"]()
        if hasattr(val, 'name'):
            val = val.name
        return str(val)

    def get_sys_variable(self, var_name: str) -> str:
        val = self.sys_var_map[var_name + "_getter"]()
        if hasattr(val, 'name'):
            val = val.name
        return str(val)

    def _thread_run_task(self):
        """ run all tasks in multiple threads """
        while True:
            next_steps = self.step_controller.next_steps()
            if next_steps is None or len(next_steps) == 0:
                break
            all_step_task = [self.thread_pool.submit(next_step.execute) for next_step in next_steps]
            wait(all_step_task, return_when=ALL_COMPLETED)
            for step_task in all_step_task:
                status = step_task.result()
                # print("status:{}".format(status))

    def _single_thread_run_task(self):
        """ run all task in single thread, used in simulation situation """
        start_time = datetime.datetime.now()
        self._print_to_screen(UserMsg.TIMER_TEMPLATE.format(start_time))

        current_steps = {}
        next_steps = self.step_controller.next_steps()
        for next_step in next_steps:
            current_steps[next_step.step_name] = next_step
        prev_time_ms = int(round(time.time() * 1000))

        while len(current_steps) > 0:
            for key, step in list(current_steps.items()):
                res = step.execute_frame()
                if res is False:
                    ''' cur step finish, add new available steps '''
                    del current_steps[key]
                    next_steps = self.step_controller.next_steps()
                    if next_steps is None or len(next_steps) == 0:
                        end_time = datetime.datetime.now()
                        self._print_to_screen(UserMsg.TIMER_TEMPLATE.format(end_time))
                        time_interval = end_time - start_time
                        self._print_to_screen(UserMsg.TIME_INTERVAL_TEMPLATE.format(time_interval))
                        return
                    for next_step in next_steps:
                        current_steps[next_step.step_name] = next_step

            fps_max = SysVar().var_map["FPS"]
            delta_time_minimum = 1.0 / fps_max

            cur_time_ms = int(round(time.time() * 1000))
            delta_time_ms = cur_time_ms - prev_time_ms
            if delta_time_ms < delta_time_minimum:
                SysVar().var_map["CUR_FPS"] = -1.0
            else:
                cur_fps = 1000.0 / delta_time_ms
                SysVar().var_map["CUR_FPS"] = cur_fps

            delta_time_std_ms = 1000.0 / fps_max
            if delta_time_std_ms - delta_time_ms > 0.1 * delta_time_std_ms:
                time.sleep((delta_time_std_ms - delta_time_ms) * 0.001)
            prev_time_ms = cur_time_ms

        end_time = datetime.datetime.now()
        self._print_to_screen(UserMsg.TIMER_TEMPLATE.format(end_time))
        time_interval = end_time - start_time
        self._print_to_screen(UserMsg.TIME_INTERVAL_TEMPLATE.format(time_interval))

    def _init_endpoint(self):
        asyncio.get_event_loop().run_until_complete(self.serve())

    def _init_sys_var_map(self):
        def schedule_mode_getter(): return self.step_controller.schedule_mode

        def schedule_mode_setter(val): self.step_controller.schedule_mode = val

        def fps_getter(): return SysVar().var_map["FPS"]

        def fps_setter(val): SysVar().var_map["FPS"] = int(val)

        self.sys_var_map = {
            "schedule_mode_getter": schedule_mode_getter,
            "schedule_mode_setter": schedule_mode_setter,
            "fps_getter": fps_getter,
            "fps_setter": fps_setter
        }

    def _load_wrapper_to_core(self):
        wrapper_list = wrapper_raw_t
        for wrapper in wrapper_list:
            ProtocolGeneric().append_wrapper(wrapper)

    def _load_monitor_config(self):
        """ load user-defined watch and alarm attribute """
        watch_list_func = import_dynamic(Config.USER_DEFINED_PACKAGE, UserDefined.WATCH_FUNC)
        alarm_list_func = import_dynamic(Config.USER_DEFINED_PACKAGE, UserDefined.ALARM_FUNC)
        ProtocolGeneric().watch_list = watch_list_func()
        ProtocolGeneric().alarm_list = alarm_list_func()

    def _load_mock_config(self):
        """ load mock bio object and operation """
        mock_func = import_dynamic(Config.USER_DEFINED_PACKAGE, UserDefined.MOCK_FUNC)
        mock_bio_obj_map, mock_op_map = mock_func()
        ProtocolGeneric().mock_bio_obj_map = mock_bio_obj_map
        ProtocolGeneric().mock_op_map = mock_op_map

    def _load_user_defined_package(self):
        """ all user defined function or class name into system """

        mod = sys.modules[Config.USER_DEFINED_PACKAGE]
        overload_msg = ""

        for name, obj in inspect.getmembers(mod):
            if (inspect.isclass(obj) or inspect.isfunction(obj)) \
                    and re.match(Config.USER_DEFINED_PACKAGE + '.*', obj.__module__) is not None:
                ProtocolGeneric().add_overload_obj(name)
                overload_msg += name + " "
        self._print_to_screen(UserMsg.SYS_SCAN_USER_DEFINED_OVERLOAD_TEMPLATE.format(overload_msg))

    def _scan_env(self):
        for wrapper in ProtocolGeneric().wrappers:
            if wrapper.get_wrapper_type() == ConstWrapper.STEP_WRAPPER:
                pass
        self.step_controller = StepController(schedule_mode=ScheduleMode.GRAPH, root_step=ProtocolGeneric().root_step)
        self.step_controller.add_step_list(ProtocolGeneric().steps_generic[1:])
        self.step_controller.print_step_tree()
        self.step_controller.add_step_list_to_graph(ProtocolGeneric().steps_generic[1:])
        self.report_gen.add_dependency_graph(ProtocolGeneric().dependency_graph_generic)

    def _run_prepare_periphery(self):
        self._print_to_screen(UserMsg.RUN_PREPARE_START_TEMPLATE.format("periphery"))
        periphery_list = ProtocolGeneric().periphery_generic
        for periphery in periphery_list:
            periphery.prepare()
        self._print_to_screen(UserMsg.RUN_PREPARE_END_TEMPLATE.format("periphery"))

    def print_sys_init_log(self):
        self.step_controller.print_step_tree()

    def _print_to_screen(self, msg: str, code=SysStatus.SUCCESS, level=MsgLevel.INFO):
        bus.emit(event=EventName.SCREEN_PRINT_EVENT,
                 msg=Msg(msg=msg, source=MsgEndpoint.SYS, destinations=[MsgEndpoint.USER_TERMINAL],
                         code=code, level=level))


def import_dynamic(module_name, target_name):
    """ dynamic specific func or class from module """
    try:
        module = __import__(module_name, fromlist=[target_name])
    except ImportError:
        raise ModuleNotFoundException(module_name)
    try:
        target = getattr(module, target_name)
    except AttributeError:
        raise ClassNotFoundException(target_name)
    return target


def import_module(module_name):
    """ load basic modules """
    try:
        __import__(module_name)
    except ImportError:
        raise ModuleNotFoundException(module_name)
