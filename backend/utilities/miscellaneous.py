import asyncio
import sys
from uuid import UUID

from loguru import logger

from utilities.serverUtilities import cache


def initLogger():
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{file.name}</cyan> | "
               "{message}",
        colorize=True)


class Stats:
    # Store currently running servers UUId
    runningServers: list[UUID] = []
    # TODO: Change to 30 if I forgot
    delay = 5
    averagePerfs: list[dict | None] = [{"cpu": 0, "ram": 0}] * int((60 / delay) * 30)

    @classmethod
    async def startPerfsLoop(cls):
        while True:
            totalRam = 0
            totalCpu = 0

            if cls.runningServers:
                for runningServer in cls.runningServers:
                    curServerManager = cache.getCurrentServerAndSm(runningServer)[
                        "serverManager"]
                    perfs = curServerManager.getPerfs()
                    totalCpu += float(perfs["cpu"])
                    totalRam += float(perfs["ram"])

                cls.averagePerfs.append({
                    "cpu": totalCpu / len(cls.runningServers),
                    "ram": totalRam / len(cls.runningServers),
                })
            else:
                cls.averagePerfs.append({
                    "cpu": 0,
                    "ram": 0,
                })

            # max lists elem fills last 30 mins
            while len(cls.averagePerfs) > (60 / cls.delay) * 30:
                cls.averagePerfs.pop(0)

            for i, perf in enumerate(cls.averagePerfs):
                perf["label"] = i

            await asyncio.sleep(cls.delay)
