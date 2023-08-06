from queue import Queue
from time import sleep

from kiwi.util import EventBus
from kiwi.common import EventName, Msg, Config, MsgLevel, SysSignal
from kiwi.core.kiwi_sys import KiwiSys
from kiwi.core.bio_op import BioOp
from termcolor import colored
from colorama import init
import datetime

bus = EventBus()


class Cmd:
    def __init__(self, callback_sys: KiwiSys):
        self.output = Output(Config.OUTPUT_MSG_BUFFER_SIZE, Config.TERMINAL_VISIBLE_LEVEL)
        self.callback_sys = callback_sys
        init()

    def run(self):
        while True:
            try:
                raw_cmd = input("kiwi>")
                self._parse_cmd(raw_cmd)
            except (KeyboardInterrupt, EOFError):
                """ stop print to screen """
                self.output.set_can_print(False)

    def _parse_cmd(self, raw_cmd: str):
        cmd_segments = raw_cmd.split(' ')
        if cmd_segments[0] == "help":
            pass
        elif cmd_segments[0] == "load":
            self.callback_sys.load_module()
        elif cmd_segments[0] == "scan":
            self.callback_sys.task_scanner()
        elif cmd_segments[0] == "run":
            self.callback_sys.run_task(False)
        elif cmd_segments[0] == "auto":
            self.callback_sys.load_module()
            self.callback_sys.task_scanner()
            self.callback_sys.run_task(False)
        elif cmd_segments[0] == "validate":
            self.callback_sys.load_module()
            self.callback_sys.task_scanner()
            self.callback_sys.run_task(True)
        elif cmd_segments[0] == "print":
            if cmd_segments[1] == "-o":
                self.output.set_can_print(True)
            elif cmd_segments[1] == "-c":
                self.output.set_can_print(False)
        elif cmd_segments[0] == "gen":
            if cmd_segments[1] == "process":
                filename = cmd_segments[2]
                self.callback_sys.report_gen_graph_topology(filename)
            elif cmd_segments[1] == "report":
                filename = cmd_segments[2]
                self.callback_sys.report_gen_html(filename)
        elif cmd_segments[0] == "ctrl":
            if cmd_segments[1] == "-sp" and cmd_segments[3] == "-op":
                """ send signal """
                step_name = cmd_segments[2]
                operation_index = cmd_segments[4]
                do_cmd = cmd_segments[5]
                sig = Cmd._cmd_param_to_signal(do_cmd)
                bus.emit(event=EventName.OP_SIGNAL_RECEIVE_EVENT
                         .format(BioOp.get_op_identifier(step_name=step_name, op_index=int(operation_index))),
                         signal=sig)
            elif cmd_segments[1] == "show":
                pass
        elif cmd_segments[0] == "sys":
            if cmd_segments[1] == "show":
                var_name = cmd_segments[2]
                var_value = self.callback_sys.get_sys_variable(var_name)
                self.output.raw_print_screen("{} = \n{}".format(var_name, var_value))
            elif cmd_segments[1] == "set":
                var_name = cmd_segments[2]
                var_value = cmd_segments[3]
                var_value = self.callback_sys.set_sys_variable(var_name, var_value)
                self.output.raw_print_screen("{} = \n{}".format(var_name, var_value))

    @staticmethod
    def _cmd_param_to_signal(param: str) -> SysSignal:
        sig = -1
        if param == "s":
            sig = SysSignal.STOP
        elif param == "r":
            sig = SysSignal.RUN
        elif param == "p":
            sig = SysSignal.SUSPEND
        elif param == "k":
            sig = SysSignal.KILL
        elif param == "c":
            sig = SysSignal.CONTINUE
        return sig


class Output:
    """ output is not thread-safe """

    def __init__(self, buffer_size: int, visible_level=MsgLevel.INFO):
        self.out_buffer = Queue(buffer_size)
        self.can_print = True
        self.visible_level = visible_level
        bus.add_event(func=self.print_screen, event=EventName.SCREEN_PRINT_EVENT)

    def printer(self):
        while True:
            if self.can_print:
                msg = self.out_buffer.get()
                print(msg)
            else:
                sleep(0.5)

    def print_screen(self, msg: Msg):
        if msg.level >= self.visible_level:
            raw_str = Output._msg_out_string(msg)
            self.out_buffer.put(raw_str)

    def raw_print_screen(self, raw_str: str):
        self.out_buffer.put(raw_str)

    def set_can_print(self, can_print: bool):
        """ output print buffered msg when open again """
        if not self.can_print:
            msg_num = self.out_buffer.qsize()
            for i in range(msg_num):
                if self.out_buffer.empty():
                    break
                msg = self.out_buffer.get()
                print(msg)
        self.can_print = can_print

    @staticmethod
    def _msg_out_string(msg: Msg):
        spec_str = " [src:" + msg.source + " destinations:"
        for destination in msg.destinations:
            spec_str += destination + ","
        if len(msg.destinations) > 0:
            spec_str = spec_str[:-1]
        spec_str += "]"
        ret = "[" + str(msg.level.name) + "][" + str(msg.code.name) + "][" + str(
            datetime.datetime.now()) + "] " + msg.msg + spec_str
        ''' color msg'''
        if msg.level == MsgLevel.IMPORTANT:
            ret = colored(ret, 'red', 'on_cyan')
        elif msg.level == MsgLevel.WARN:
            ret = colored(ret, 'red', 'on_green')
        return ret
