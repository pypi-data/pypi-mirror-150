
class ImageWriter:

    def __init__(self, remote):
        self._remote = remote

    async def write_sequence(self, walker, acquisition_name):
        """Wrap the walker and write data."""
        async with walker:
            try:
                walker.descend(acquisition_name)
                await self._remote.start(walker)
            finally:
                walker.ascend()

    async def wait(self, count):
        await self._remote.wait(count)

    # def _teardown(self):
    #     self._remote.

