from kiwi.util import TreeAryN, EventBus, DAG
from kiwi.common import sort_default, EventName, SysStatus, ScheduleMode, TypeErrorException
from typing import List
from .step import Step
import random

bus = EventBus()


class Strategy:

    @staticmethod
    def next_object_random(schedule_list: []) -> [Step]:
        return [schedule_list[random.randint(0, len(schedule_list) - 1)]]

    @staticmethod
    def next_first(schedule_list: []) -> [Step]:
        return [schedule_list[0]]

    @staticmethod
    def next_all(schedule_list: []) -> [Step]:
        available_list = Strategy.exclusive_predicate(schedule_list)
        available_ids = "available ids:"
        for step in available_list:
            available_ids += step.step_name + " "
        print(available_ids)
        return available_list

    @staticmethod
    def exclusive_predicate(schedule_list: []) -> [Step]:
        available_list = []
        max_count = 0
        sum_num = len(schedule_list)
        for i in range(0, sum_num):
            tmp_available_list = []
            tmp_count = 0
            tmp_set = set()

            for j in range(i, sum_num):
                exclusive_ids = schedule_list[j].get_exclusive_obj_ids()
                flag = False
                for ex_id in exclusive_ids:
                    if ex_id in tmp_set:
                        flag = True
                        break
                if flag is True:
                    continue
                for ex_id in exclusive_ids:
                    tmp_set.add(ex_id)
                tmp_count = tmp_count + 1
                tmp_available_list.append(schedule_list[j])
            if tmp_count > max_count:
                max_count = tmp_count
                available_list = tmp_available_list
        return available_list

    @staticmethod
    def score_average_first(schedule_list: []) -> [Step]:
        return schedule_list


class StepController:
    def __init__(self, schedule_mode: ScheduleMode, root_step: Step):
        self.step_tree = TreeAryN(sort_func=sort_default)
        self.step_graph = DAG()
        self._schedule_mode = schedule_mode
        self.step_tree.add_node(root_step)
        self.step_graph.add_node(root_step)

    def add_step_list(self, steps: List[Step]):
        un_auto_step_name = "0"
        prev_auto_step_name = "0"
        for step in steps:
            if step.step_name == "-1":
                ''' auto increase step '''
                if prev_auto_step_name == "0":
                    prev_auto_step_name = un_auto_step_name + ".0"
                auto_step_name = Step.next_child_step(prev_auto_step_name)
                step.step_name = auto_step_name
                step.key = auto_step_name
                prev_auto_step_name = auto_step_name
            else:
                un_auto_step_name = step.step_name
                prev_auto_step_name = "0"

            parent_step_key = Step.parent_step(step.step_name)
            self.step_tree.add_node(step, parent_step_key)
            print(step.step_name)

    def add_step_list_to_graph(self, steps: List[Step]):
        for step in steps:
            self.step_graph.add_node(step)
        for step in steps:
            parent_step = Step.parent_step(step.step_name)
            self.step_graph.add_edge_by_key(parent_step, step.step_name)
            younger_brother_step = Step.brother_step(step.step_name, True)
            if younger_brother_step is not None:
                self.step_graph.add_edge_by_key(younger_brother_step, step.step_name)
            wait_list = step.wait_list
            for wait_step_num in wait_list:
                self.step_graph.add_edge_by_key(wait_step_num, step.step_name)
        for step in steps:
            parallel_list = step.children_parallel_list
            for pa_i in parallel_list:
                for pa_j in parallel_list:
                    if self.step_graph.is_edge_exist(pa_i, pa_j):
                        self.step_graph.delete_edge_by_key(pa_i, pa_j)

    def next_steps(self) -> [Step]:
        schedule_list = list()
        ''' get steps that are available '''
        if self._schedule_mode == ScheduleMode.SEQ:
            schedule_list = self.step_tree.preorder(exclude_done=True)
        elif self._schedule_mode == ScheduleMode.GRAPH:
            schedule_list = self.step_graph.available_nodes()
        if len(schedule_list) == 0:
            return None
        ''' choose steps according to strategy '''
        if self._schedule_mode == ScheduleMode.SEQ:
            return Strategy.next_first(schedule_list)
        elif self._schedule_mode == ScheduleMode.GRAPH:
            return Strategy.next_all(schedule_list)
        return []

    def seq_steps(self) -> [Step]:
        return self.step_tree.preorder()

    def print_step_tree(self):
        print("\n===================step tree===================")
        print(self.step_tree)
        print("=================step tree end=================\n")

    @bus.on(event=EventName.STEP_EVENT)
    def _listen_step(self, step_name: str, step_status: SysStatus):
        pass

    @property
    def schedule_mode(self):
        return self._schedule_mode

    @schedule_mode.setter
    def schedule_mode(self, schedule_mode):
        if type(schedule_mode) == str:
            schedule_mode = ScheduleMode(int(schedule_mode))
        elif type(schedule_mode) == int:
            schedule_mode = ScheduleMode(schedule_mode)
        else:
            raise TypeErrorException(expect_type=type(ScheduleMode), actual_type=type(schedule_mode))
        self._schedule_mode = schedule_mode
