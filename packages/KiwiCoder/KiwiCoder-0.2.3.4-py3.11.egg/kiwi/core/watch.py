import asyncio

from kiwi.common.common import singleton

from kiwi.common.message import Msg

from kiwi.common.constant import MsgEndpoint, EventName, MsgLevel, SysStatus

from kiwi.util.event import EventBus

bus = EventBus()


@singleton
class Watcher:
    def __init__(self):
        """ multiple queues and rpc is used due to different amount of msg """
        self.bio_comm_msg = asyncio.Queue()
        self.protocol_msg = asyncio.Queue()
        bus.add_event(func=self.dispatch_watch_msg, event=EventName.WATCH_EVENT)

    def dispatch_watch_msg(self, src: str, raw_msg: str, level=MsgLevel.GOSSIP):
        asyncio.run(self._dispatch_watch_msg(src, raw_msg, level))

    async def _dispatch_watch_msg(self, src: str, raw_msg: str, level=MsgLevel.GOSSIP):
        bus.emit(event=EventName.SCREEN_PRINT_EVENT, msg=Msg(msg=raw_msg, source=src,
                                                             destinations=[MsgEndpoint.USER_TERMINAL],
                                                             code=SysStatus.SUCCESS, level=level))
        if src == MsgEndpoint.BIO_OBJ:
            await self.bio_comm_msg.put((src, raw_msg))

        if src == MsgEndpoint.OP or src == MsgEndpoint.STEP:
            await self.bio_comm_msg.put((src, raw_msg))
            await self.protocol_msg.put((src, raw_msg))
