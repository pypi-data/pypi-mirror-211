import asyncio
from threading import Thread

from kiwi.cli.command import Cmd
from kiwi.core.kiwi_sys import KiwiSys
from kiwi.common import ScheduleMode


class KiwiCoder:
    def __init__(self):
        self.kiwi_sys = KiwiSys(thread_pool_size=10, schedule_mode=ScheduleMode.GRAPH)
        self.cmd = Cmd(self.kiwi_sys)

    def __del__(self):
        if self.cmd_thread is not None:
            self.cmd_thread.join()
        if self.printer_thread is not None:
            self.printer_thread.join()

    def run(self) -> None:
        self._run_printer()
        self._run_cmd()
        self._run_ws_server()
        self._run_http()
        self.kiwi_sys.build_sys()

    def run_all(self) -> None:
        self._run_printer()
        self.kiwi_sys.build_sys()
        self.kiwi_sys.task_scanner()
        self.kiwi_sys.run_task(False)

    def _run_cmd(self) -> None:
        self.cmd_thread = Thread(target=self.cmd.run)
        self.cmd_thread.start()

    def _run_printer(self) -> None:
        self.printer_thread = Thread(target=self.cmd.output.printer)
        self.printer_thread.start()

    def _run_ws_server(self) -> None:
        def asyncio_run(kiwi_sys): asyncio.run(kiwi_sys.ws_server.serve())
        self.ws_server_thread = Thread(target=asyncio_run, args=(self.kiwi_sys,))
        self.ws_server_thread.start()

    def _run_http(self) -> None:
        self.http_server_thread = Thread(target=self.kiwi_sys.http_server.serve)
        self.http_server_thread.start()

