"""
Remote add-ons working on image streams directly.
"""
import pickle
from concert.experiments.proxies.base import Proxy


class TangoProxy(Proxy):
    def __init__(self, tango_device):
        self._device = tango_device

    async def wait(self, count):
        await self._device.wait(count)


def ImageWriter(device):
    return device
