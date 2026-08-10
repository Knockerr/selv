import asyncio
import sys
from uuid import UUID

from loguru import logger
from typing import Literal
from utilities import db
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
    delay = 5
    averagePerfs: list[dict | None] = [{"cpu": 0, "ram": 0}] * int((60 / delay) * 30)

    @classmethod
    async def getAveragePerfs(cls):
        totalRam = 0
        totalCpu = 0

        if cls.runningServers:
            for runningServer in cls.runningServers:
                curServerManager = cache.getCurrentServerAndSm(runningServer)[
                    "serverManager"]
                perfs = curServerManager.getPerfs()
                totalCpu += float(perfs["cpu"])
                totalRam += float(perfs["ram"])
            return {
                    "cpu": totalCpu / len(cls.runningServers),
                    "ram": totalRam / len(cls.runningServers),
                }
        else:
            return {
                    "cpu": 0,
                    "ram": 0,
                }

    @classmethod
    async def startPerfsLoop(cls):
        while True:
            averagePerfs = await cls.getAveragePerfs()
            cls.averagePerfs.append(averagePerfs)

            # max lists elem fills last 30 mins
            while len(cls.averagePerfs) > (60 / cls.delay) * 30:
                cls.averagePerfs.pop(0)

            for i, perf in enumerate(cls.averagePerfs):
                perf["label"] = i

            await asyncio.sleep(cls.delay)

    @classmethod
    async def trackPerfs(cls, delay=5, sendLabel: bool = False, content: Literal["all", "last"] = "all"):
        while True:
            if content == "all":
                perfs = cls.averagePerfs
                if not sendLabel:
                    for perf in perfs:
                        if "label" in perf:
                            del perf["label"]
                yield perfs
            else:
                currentPerf = await cls.getAveragePerfs()
                yield currentPerf

            await asyncio.sleep(delay)

    @classmethod
    def _getServersDatas(cls):
        conn = db.getConnexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM servers")
        servers: list[dict] = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return servers

    @classmethod
    def getServersTypesDstrib(cls):
        types = {}
        servers = cls._getServersDatas()
        for server in servers:
            serverType = server["serverType"]
            if serverType in types:
                types[serverType] += 1
            else:
                types[serverType] = 1
        return types

    @classmethod
    def getServersTotalUptime(cls):
        totalUptime: int = 0
        allServersDatas = cls._getServersDatas()
        for server in allServersDatas:
            totalUptime += server["uptime"] or 0
        return totalUptime

    @classmethod
    def getServersUptime(cls):
        uptimes = {}
        allServersDatas = cls._getServersDatas()
        for server in allServersDatas:
            uptimes[server["name"]] = server["uptime"] or 0
        return uptimes
