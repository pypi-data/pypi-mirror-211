from abc import abstractmethod

from kiwi.core.bio_quantity import Volume, Temperature

from kiwi.common.constant import ContainerType, PeripheryUsage

from kiwi.common import ConstWrapper, ParseParamException

wrapper_raw_t = []


class Wrapper:

    def __init__(self, wrapper_type, *args, **kwargs):
        """attach the wrapper to environment"""
        self.id = -1  # same as id in core object
        self.wrapper_type = wrapper_type
        self.args = args
        self.kwargs = kwargs
        self.core_obj = None
        wrapper_raw_t.append(self)

    def inject_core_obj(self, core_obj):
        self.core_obj = core_obj

    def get_id(self):
        return self.id

    def get_wrapper_type(self):
        return self.wrapper_type

    @abstractmethod
    def package_name(self) -> str:
        pass

    def class_name(self) -> str:
        return self.__class__.__name__


# ==================================== #
#        Protocol Framework            #
# ==================================== #

class Step(Wrapper):
    def __init__(self, name: str, step_spec="", repeat_times=1):
        step_name, wait_list, parallel_list = Step._parse_step_spec(step_spec)
        super().__init__(name=name, step_name=step_name, wait_list=wait_list, children_parallel_list=parallel_list,
                         repeat_times=repeat_times, wrapper_type=ConstWrapper.STEP_WRAPPER)
        self.name = name
        self.step_spec = step_spec
        self.repeat_times = repeat_times

    @staticmethod
    def _parse_step_spec(step_spec: str) -> (str, [str], [str]):
        """
            step_spec: a string which denotes step num, wait list, and parallel list.
            step number: step hierarchy, e.g. 1.2.1
            wait list: the step must run after all the steps and its previous step finish, e.g. [1.1,2.3]
            children parallel list: the child steps of it can run in parallel. e.g [1.1,1.2,1.3]
            a simple example: sn:2 wt:[1.1] cp[2.1,2.2,2.3]
            this step is 2rd step, it can run after 1.1 finish, and 2.1,2.2,2.3 steps can run in parallel
            if sn is -1, the step number will increase automatically
        """
        sn = None
        wt = []
        cp = []
        param_list = step_spec.split(' ', 3)
        if len(param_list) > 3 or len(param_list) == 0:
            raise ParseParamException('param numbers is wrong')

        for i in range(0, len(param_list)):
            if param_list[i][0:3] == "sn:":
                sn = param_list[i][3:]
            elif param_list[i][0:3] == "wt:":
                wt_raw = param_list[i][4:-1]
                wt = wt_raw.split(',')
            elif param_list[i][0:3] == "cp:":
                cp_raw = param_list[i][4:-1]
                cp = cp_raw.split(',')
            else:
                raise ParseParamException('param is wrong')

        return sn, wt, cp

    def package_name(self) -> str:
        return "kiwi.core"


# ==================================== #
#              Bio Entity              #
# ==================================== #


class Container(Wrapper):
    def __init__(self, container_type: ContainerType, name="", fluid=None, volume=Volume(Volume.max_val, "ml"),
                 sample_io_peripheries=None):
        super().__init__(container_type=container_type, name=name, fluid=fluid, volume=volume,
                         sample_io_peripheries=sample_io_peripheries, wrapper_type=ConstWrapper.ENTITY_CONTAINER_WRAPPER)

    def package_name(self) -> str:
        return "kiwi.core.bio_entity"


class Column(Wrapper):
    pass


class Slide(Wrapper):
    pass


class Fluid(Wrapper):
    def __init__(self, name: str, state=None, temp=Temperature.ROOM, volume=None, sample_io_peripheries=None):
        super().__init__(name=name, state=state, temp=temp, volume=volume,
                         sample_io_peripheries=sample_io_peripheries, wrapper_type=ConstWrapper.ENTITY_FLUID_WRAPPER)

    def package_name(self) -> str:
        return "kiwi.core.bio_entity"


class Solid(Wrapper):
    pass


class Plate(Wrapper):
    pass


class Tissue(Wrapper):
    pass


# ==================================== #
#        Protocol Hardware             #
# ==================================== #

class Periphery(Wrapper):
    def __init__(self, company: str, product: str, wrapper_type, comment: str, name: str = "",
                 usage=PeripheryUsage.BASE, *init_args,
                 **init_kwargs):
        """
        Periphery Wrapper can run only when company & pn are specified
        Args:
            company: which company produce the product
            product: the product number unique in a company
        """
        self.company = company
        self.product = product
        self.comment = comment
        super().__init__(name=name, usage=usage, wrapper_type=wrapper_type, *init_args, **init_kwargs)

    @abstractmethod
    def package_name(self) -> str:
        pass

    def class_name(self) -> str:
        comm_name = ConstWrapper.get_class_name(self.wrapper_type)
        return comm_name + self.company + self.product


class ControlPeriphery(Periphery):
    def __init__(self, company: str, product: str, comment: str, name: str = "", usage=PeripheryUsage.BASE, *init_args,
                 **init_kwargs):
        super().__init__(company=company, product=product, wrapper_type=ConstWrapper.PERIPHERY_CONTROL_WRAPPER,
                         comment=comment, name=name, usage=usage,
                         *init_args, **init_kwargs)

    def package_name(self) -> str:
        return "kiwi.plugin.hardware.control"


class InstrumPeriphery(Periphery):
    def __init__(self, company: str, product: str, comment: str, name: str = "", usage=PeripheryUsage.BASE, *init_args,
                 **init_kwargs):
        super().__init__(company=company, product=product, wrapper_type=ConstWrapper.PERIPHERY_INSTRUM_WRAPPER,
                         comment=comment, name=name, usage=usage,
                         *init_args, **init_kwargs)

    def package_name(self) -> str:
        return "kiwi.plugin.hardware.instrum"


class SignalPeriphery(Periphery):
    def __init__(self, company: str, product: str, comment: str, name: str = "", usage=PeripheryUsage.BASE, *init_args,
                 **init_kwargs):
        super().__init__(company=company, product=product, wrapper_type=ConstWrapper.PERIPHERY_SIGNAL_WRAPPER,
                         comment=comment, name=name, usage=usage,
                         *init_args, **init_kwargs)

    def package_name(self) -> str:
        return "kiwi.plugin.hardware.signal"
