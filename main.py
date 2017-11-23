from tornado import gen
from tornado.ioloop import IOLoop
from tornado.tcpclient import TCPClient
import sys


class Fonar:

    def __init__(self, default_color):
        self.flag_on = 0
        self.color = default_color
        self.host = "localhost"
        self.port = 9999
        self.max_bytes = 6

    def set_host_port(self, host, port):
        self.host = host
        self.port = port

    @gen.coroutine
    def run(self):
        stream = yield TCPClient().connect(self.host, self.port)
        try:
            while True:
                yield self.react(stream)
        except KeyboardInterrupt:
            stream.close()

    @gen.coroutine
    def react(self, stream):
        message = yield stream.read_bytes(self.max_bytes)

        type = message[0]

        if type == 0x12:
            self.flag_on = 1

        elif type == 0x13:
            self.flag_on = 0

        elif type == 0x20:
            changed_color = message[3:6]
            self.color = changed_color


if __name__ == '__main__':

    fonar = Fonar(b'123')

    if len(sys.argv) > 1:
        host = sys.argv[1]
        port = sys.argv[2]
        fonar.set_host_port(host, port)

    IOLoop.instance().start()
    try:
        IOLoop.instance().run_sync(fonar.run)
    except KeyboardInterrupt:
        IOLoop.instance().stop()
