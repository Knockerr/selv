import asyncio
from typing import Callable
from uuid import UUID

from loguru import logger


class EventBus:
    def __init__(self):
        self.subscribers: list[Callable] = []
        self.currentVal = None

    def setValue(self, currentValue: str or dict or None = None):
        self.currentVal = currentValue

    def subscribe(self, callback: Callable):
        self.subscribers.append(callback)
        _ = asyncio.create_task(self.broadcast(self.currentVal))

    def unsubscribe(self, callback: Callable):
        self.subscribers.remove(callback)

    async def broadcast(self, data: str or dict):
        self.currentVal = data
        for subscriber in self.subscribers:
            await subscriber(data)


serversStatesBuses: dict[UUID, EventBus] = {}


def getServerBus(uuid):
    """
    defaultValue will only be used if no EventBus exists for uuid
    """
    if uuid not in serversStatesBuses:
        serversStatesBuses[uuid] = EventBus()
    return serversStatesBuses[uuid]
