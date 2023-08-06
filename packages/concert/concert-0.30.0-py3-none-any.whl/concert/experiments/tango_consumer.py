#!/usr/bin/python
"""
Tango server for elmo_main.py-controller based motors
"""
import asyncio
import concert.writers
import numpy as np
import pickle
import time
import tango
import zmq
import zmq.asyncio
from concert.coroutines.base import start
from concert.helpers import PerformanceTracker
from concert.quantities import q
from concert.storage import DirectoryWalker
from tango import InfoIt, DebugIt
from PyTango.server import Device, attribute, DeviceMeta, pipe
from PyTango.server import AttrWriteType, command, device_property
from PyTango import DevState
from PyTango import ArgType, AttrDataFormat


async def coro():
    print('start')
    await asyncio.sleep(5)
    print('end')

    return 'done'


class DummyMotor(Device):
    """
    Device server for elmo_main.py-controller based
    """
    __metaclass__ = DeviceMeta
    volume = attribute(label="Volume", dtype=((np.float32,),),
            max_dim_x=1024, max_dim_y=1024,
                         access=AttrWriteType.READ,
                         fget="get_volume")

    endpoint = attribute(label="Endpoint", dtype=str,
                         access=AttrWriteType.READ_WRITE,
                         fget="get_endpoint", fset="set_endpoint")

    writer_class = attribute(label="Writerclass", dtype=str,
                         access=AttrWriteType.READ_WRITE,
                         fget="get_writer_class", fset="set_writer_class")

    dsetname = attribute(label="Dsetname", dtype=str,
                         access=AttrWriteType.READ_WRITE,
                         fget="get_dsetname", fset="set_dsetname")

    bytes_per_file = attribute(label="bytes_per_file", dtype=int,
                         access=AttrWriteType.READ_WRITE,
                         fget="get_bytes_per_file", fset="set_bytes_per_file")

    def __init__(self, a, b):
        self._context = zmq.asyncio.Context()
        self._socket = None
        self._task = None
        self._stop_at = None
        self._endpoint = None
        self._path = None
        # Walker
        self._writer_class = 'TiffWriter'
        self._dsetname = 'frame_{:>06}.tif'
        self._bytes_per_file = 2 ** 40
        super().__init__(a, b)

    async def init_device(self):
        """Inits device and communciation"""
        self.debug_stream("Init device")
        super().init_device()
        if self.get_state() == tango.DevState.RUNNING:
            self.debug_stream("Cancelling task: %s", self._task.cancel())
        # await self.disconnect_zmq()
        # print(self._socket, self._endpoint)
        if self._endpoint and not self._socket:
            await self.setup()
        self.set_state(tango.DevState.STANDBY)

    @DebugIt()
    @command()
    async def setup(self):
        if not self._endpoint:
            raise RuntimeError('Cannot connect when endpoint is not specified')

        if self._socket:
            self._socket.close()

        self._socket = self._context.socket(zmq.PULL)
        self._socket.connect(self._endpoint)
        

    @DebugIt()
    @command()
    async def teardown(self):
        if self._socket:
            self._socket.close()
            self._socket = None

    @InfoIt()
    async def get_endpoint(self):
        return self._endpoint

    @InfoIt(show_args=True)
    async def set_endpoint(self, endpoint):
        if self._endpoint == endpoint:
            return

        self._endpoint = endpoint
        await self.setup()

    @DebugIt()
    @command(dtype_in=str)
    def set_path(self, path):
        self._path = path

    @DebugIt()
    @command()
    def write_sequence(self):
        def callback(task):
            self.debug_stream('start callback, cancelled: %s, exception: %s',
                              task.cancelled(), task.exception())
            self.set_state(tango.DevState.STANDBY)
        walker = DirectoryWalker(
            writer=getattr(concert.writers, self._writer_class),
            dsetname=self._dsetname,
            bytes_per_file=self._bytes_per_file,
            root=self._path
        )
        self._stop_at = None
        self._task = start(self.consume(walker))
        self._task.add_done_callback(callback)
        self.set_state(tango.DevState.RUNNING)

    @DebugIt(show_args=True)
    @command(dtype_in=int)
    async def wait(self, num):
        self._stop_at = num
        if self._task is None:
            raise RuntimeError('Not started')

        try:
            await self._task
        finally:
            self._task = None
            self._stop_at = None

    async def consume(self, walker):
        with PerformanceTracker() as pt:
            total_bytes = await walker.write(self.subscribe())
            pt.size = total_bytes * q.B

    @InfoIt()
    def get_writer_class(self):
        return self._writer_class

    @InfoIt()
    def set_writer_class(self, writer_class):
        self._writer_class = writer_class

    @InfoIt()
    def get_dsetname(self):
        return self._dsetname

    @InfoIt()
    def set_dsetname(self, dsetname):
        self._dsetname = dsetname

    @InfoIt()
    def get_bytes_per_file(self):
        return self._bytes_per_file

    @InfoIt()
    def set_bytes_per_file(self, bytes_per_file):
        self._bytes_per_file = bytes_per_file

    @InfoIt()
    def get_volume(self):
        # import numpy as np
        return np.arange(25, dtype=np.float32).reshape(5, 5)
        # return [[1, 2, 3], [4, 5, 6.]]

    async def subscribe(self):
        i = 0

        while True:
            num_tries = 0
            while True:
                # We might get None if we are faster than the sender or the stopping count is set
                # after the stream ends
                image = await self._recv_array()
                if image is None:
                    num_tries += 1
                else:
                    break
                if self._stop_at is not None and i >= self._stop_at:
                    break
            if image is None:
                print(f'Stopping at i={i:>5} (tries={num_tries:>4}), stop at: {self._stop_at}')
                break
            yield image
            i += 1
            print(f'i={i:>5} (tries={num_tries:>4}), stop at: {self._stop_at}')

    async def _recv_array(self):
        import zmq

        try:
            md = await self._socket.recv_json(flags=zmq.NOBLOCK)
            msg = await self._socket.recv()
            array = np.frombuffer(msg, dtype=md['dtype'])

            return array.reshape(md['shape'])
        except zmq.Again:
            return None


def run_server():
    DummyMotor.run_server(
            args=['name', '-ORBendPoint', 'giop:tcp::1235', '-v4', '-nodb', '-dlist', 'a/b/c'],
            green_mode=tango.GreenMode.Asyncio
        )


if __name__ == "__main__":
    run_server()
