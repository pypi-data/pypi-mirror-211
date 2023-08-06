import asyncio
import json

import websockets
from http.server import BaseHTTPRequestHandler, HTTPServer

from kiwi.common.message import Msg
from kiwi.core.globals import SysVar

from kiwi.util.event import EventBus

from kiwi.common.constant import SysStatus, EventName, UserMsg, MsgEndpoint, MsgLevel, Config

from kiwi.core.watch import Watcher

bus = EventBus()
sys_var = SysVar()


class WebSocket:
    def __init__(self, ip_address: str, port: int):
        self.msg_watch = Watcher()
        self.ip_address = ip_address
        self.port = port

    async def send_msg(self, ws) -> None:
        while True:
            msg = await self.msg_watch.bio_comm_msg.get()
            msg_raw = "{}${}${}".format("WATCH", msg[0], msg[1])
            print("cur msg:{}".format(msg))
            await ws.send(msg_raw)

    async def serve(self) -> None:
        async with websockets.serve(self.send_msg, self.ip_address, self.port):
            bus.emit(event=EventName.SCREEN_PRINT_EVENT,
                     msg=Msg(msg=UserMsg.SERVER_INIT_TEMPLATE, source=MsgEndpoint.SERVER,
                             destinations=[MsgEndpoint.USER_TERMINAL], code=SysStatus.SUCCESS, level=MsgLevel.INFO))
            await asyncio.Future()


class CustomHttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/sys_var':
            var_map = json.dumps(sys_var.var_map)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(var_map, "utf-8"))

    def do_POST(self):
        if self.path == '/sys_var':
            req_data = self.rfile.read(int(self.headers['content-length']))
            req_str = str(req_data.decode())
            var_map = json.loads(req_str)
            for k, v in var_map.items():
                sys_var.var_map[str(k)] = v
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()


class KiwiHttpServer:
    def __init__(self, ip_address: str, port: int):
        self.ip_address = ip_address
        self.port = port
        self.http_server = HTTPServer((self.ip_address, self.port), CustomHttpServer)

    def __del__(self):
        self.http_server.server_close()

    def serve(self) -> None:
        self.http_server.serve_forever()
