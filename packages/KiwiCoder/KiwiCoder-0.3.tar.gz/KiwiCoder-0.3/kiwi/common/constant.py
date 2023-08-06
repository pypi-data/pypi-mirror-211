from enum import Enum, IntEnum


class ConstWrapper(IntEnum):
    BASE_WRAPPER = 0
    STEP_WRAPPER = 1

    OP_WRAPPER = 10
    OP_MEASURE_FLUID_WRAPPER = 11
    OP_STORE_WRAPPER = 12
    OP_START_PROTOCOL_WRAPPER = 13
    OP_END_PROTOCOL_WRAPPER = 14
    OP_DO_NOTHING_WRAPPER = 15
    OP_COMMENT_WRAPPER = 16
    OP_VORTEX_WRAPPER = 17
    OP_TAP_WRAPPER = 18
    OP_DISSOLVE_WRAPPER = 19
    OP_CENTRIFUGE_PELLET_WRAPPER = 20
    OP_DIRECT_CALL_WRAPPER = 21
    OP_TRANSFER_WRAPPER = 22
    OP_WAIT_WRAPPER = 23

    ENTITY_WRAPPER = 1000
    ENTITY_CONTAINER_WRAPPER = 1001
    ENTITY_COLUMN_WRAPPER = 1002
    ENTITY_SLIDE_WRAPPER = 1003

    ENTITY_FLUID_WRAPPER = 1100
    ENTITY_PLATE_WRAPPER = 1101
    ENTITY_TISSUE_WRAPPER = 1102

    QUANTITY_WRAPPER = 1800
    QUANTITY_VOL_WRAPPER = 1801
    QUANTITY_SPEED_WRAPPER = 1802
    QUANTITY_TEMPERATURE_WRAPPER = 1803
    QUANTITY_TIME_WRAPPER = 1804

    PERIPHERY_WRAPPER = 2000
    PERIPHERY_CONTROL_WRAPPER = 2500
    PERIPHERY_INSTRUM_WRAPPER = 3000
    PERIPHERY_SIGNAL_WRAPPER = 3500

    PERIPHERY_CONTROL_PHIDGET_RELAY_WRAPPER = 2500
    PERIPHERY_INSTRUM_FLOW_METER_WRAPPER = 3001

    LIMIT = 10000

    @staticmethod
    def is_op_wrapper(wrapper_type: int) -> bool:
        return ConstWrapper.OP_WRAPPER.value <= wrapper_type < ConstWrapper.ENTITY_WRAPPER.value

    @staticmethod
    def is_quantity_wrapper(wrapper_type: int) -> bool:
        return ConstWrapper.QUANTITY_WRAPPER.value <= wrapper_type < ConstWrapper.PERIPHERY_WRAPPER.value

    @staticmethod
    def is_periphery_wrapper(wrapper_type: int) -> bool:
        return ConstWrapper.PERIPHERY_WRAPPER.value <= wrapper_type < ConstWrapper.LIMIT.value

    @staticmethod
    def is_container_wrapper(wrapper_type: int) -> bool:
        return ConstWrapper.ENTITY_WRAPPER.value <= wrapper_type < ConstWrapper.ENTITY_FLUID_WRAPPER.value

    @staticmethod
    def is_fluid_wrapper(wrapper_type: int) -> bool:
        return ConstWrapper.ENTITY_FLUID_WRAPPER.value <= wrapper_type < ConstWrapper.QUANTITY_WRAPPER.value

    @staticmethod
    def get_class_name(wrapper_type: int) -> str:
        enum_type = ConstWrapper(wrapper_type)
        enum_name = enum_type.name
        raw_name_list = enum_name.split('_')
        core_name = []
        final_name = ""
        if ConstWrapper.is_periphery_wrapper(wrapper_type):
            core_name = raw_name_list[2:-1]
        for name in core_name:
            lower_str = name.title()
            final_name += lower_str
        return final_name

    @staticmethod
    def get_op_class_name(wrapper_type: int) -> str:
        enum_type = ConstWrapper(wrapper_type)
        enum_name = enum_type.name
        raw_name_list = enum_name.split('_')[1:-1]
        final_name = ""
        for name in raw_name_list:
            name = name.lower()
            final_name += name.title()
        return final_name + "Op"


class PeripheryUsage(IntEnum):
    BASE = 0
    DRIVER = 1000
    VALVE = 1001
    MEASURE = 2000
    TRANSFER = 3000


class SysStatus(IntEnum):
    FAIL = 0
    SUCCESS = 1

    INIT = 100
    AVAILABLE = 101
    RUNNING = 102
    PENDING = 103
    DONE = 104


class MsgLevel(IntEnum):
    GOSSIP = 0
    INFO = 1
    IMPORTANT = 2
    WARN = 3
    ERROR = 4
    FATAL = 5

    @staticmethod
    def to_string(level: int) -> str:
        ret = ""
        if level == 0:
            ret = "GOSSIP"
        elif level == 1:
            ret = "INFO"
        elif level == 2:
            ret = "IMPORTANT"
        elif level == 3:
            ret = "WARN"
        elif level == 4:
            ret = "ERROR"
        elif level == 5:
            ret = "FATAL"
        return ret


class MsgEndpoint:
    OP = "op"
    STEP = "step"
    WATCH = "watch"
    USER_TERMINAL = "user_terminal"
    SYS = "sys"
    BIO_OBJ = "bio_obj"
    SERVER = "server"


class EventName:
    OP_EVENT = "event:op"
    OP_SIGNAL_RECEIVE_EVENT = "event:op:{}:sig:receive"
    STEP_EVENT = "event:step"
    FATAL_ALARM_EVENT = "event:fatal_alarm"
    SCREEN_PRINT_EVENT = "event:screen:print"
    WATCH_EVENT = "event:watch"


class AutoLevel(IntEnum):
    HUMAN = 0
    SEMI = 1
    FULL = 2


class SysSignal(IntEnum):
    STOP = 0
    RUN = 1
    SUSPEND = 2
    KILL = 3
    CONTINUE = 4


class ScheduleMode(IntEnum):
    SEQ = 0
    GRAPH = 1


class MathOp(IntEnum):
    GT = 0
    GE = 1
    EQ = 2
    NE = 3
    LT = 4
    LE = 5

    @staticmethod
    def compare(left_value, right_value, math_op) -> bool:
        if left_value is None or right_value is None:
            return False
        if math_op == MathOp.GT:
            return left_value > right_value
        elif math_op == MathOp.GE:
            return left_value >= right_value
        elif math_op == MathOp.EQ:
            return left_value == right_value
        elif math_op == MathOp.NE:
            return left_value != right_value
        elif math_op == MathOp.LT:
            return left_value < right_value
        elif math_op == MathOp.LE:
            return left_value <= right_value


class UserMsg:
    OP_OPERATE_HUMAN_TEMPLATE = "This operation(step:{} op:{}) requires human. Send 'Continue' signal when finish."
    OP_STAGE_START_TEMPLATE = "Step:{} Operation:{} Stage:{} begin."
    OP_STAGE_END_TEMPLATE = "Step:{} Operation:{} Stage:{} finish."
    OP_MOCK_START_TEMPLATE = "[MOCK] Step:{} Operation:{} Stage:{} begin."
    OP_MOCK_END_TEMPLATE = "[MOCK] Step:{} Operation:{} Stage:{} finish."
    OP_SIGNAL_TEMPLATE = "Step:{} Operation:{} receive signal :{}."
    OP_PROTOCOL_START_TEMPLATE = "Protocol:{} start"
    OP_PROTOCOL_END_TEMPLATE = "Protocol end"
    STEP_START_TEMPLATE = "Step:{} begin. Repeat times:{}. Already execute {} times."
    STEP_END_TEMPLATE = "Step:{} finish."
    STEP_VALIDATION_END_TEMPLATE = "[VALIDATE] Step:{} Op:{} finish."
    SYS_SCAN_USER_DEFINED_OVERLOAD_TEMPLATE = "Overload user-defined: {}"
    REPORT_GENERATE_TEMPLATE = "Report {} has been generated."
    RUN_PREPARE_START_TEMPLATE = "Prepare {} start."
    RUN_PREPARE_END_TEMPLATE = "Prepare {} end."
    SERVER_INIT_TEMPLATE = "Server init."
    TIMER_TEMPLATE = "Current time:{}."
    TIME_INTERVAL_TEMPLATE = "Time interval:{} seconds."


class Config:
    OUTPUT_MSG_BUFFER_SIZE = 100
    TERMINAL_VISIBLE_LEVEL = MsgLevel.GOSSIP
    USER_DEFINED_PACKAGE = "user"
    CORE_OP_PACKAGE = "kiwi.core.bio_op"
    WS_PORT = 50051
    WS_IP = "localhost"
    HTTP_PORT = 50052
    HTTP_IP = "localhost"


class UserDefined:
    MAIN_PROTOCOL_FUNC = "kiwi_protocol"
    WATCH_FUNC = "watch"
    ALARM_FUNC = "alarm"
    MOCK_FUNC = "mock"


class PlaceHolder:
    ALL = "$ALL$"
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


# ==================================== #
#            Biology type              #
# ==================================== #
class PCRType:
    pass


class UntilType:
    pass


class ContainerType:
    FAKE_CONTAINER = -1
    STERILE_MICROFUGE_TUBE = 0
    CENTRIFUGE_TUBE_15ML = 1
    FLASK = 2
    EPPENDORF = 3
