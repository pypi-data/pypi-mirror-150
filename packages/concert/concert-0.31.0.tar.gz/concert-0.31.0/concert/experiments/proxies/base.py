class Proxy:
    async def setup(self):
        pass

    async def teardown(self):
        pass

    async def wait(self, num):
        pass


class ImageWriter(Proxy):
    async def set_path(self, path):
        raise NotImplementedError
