import threading
from scapy.all import *
from time import sleep
import socket

class Transmitter(threading.Thread):
    def __init__(self, iface, filter, port=50000):
        super().__init__()
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug(f'Transmitter started: iface={iface}, filter={filter}, port={port}')
        self.iface = iface
        self.filter = filter
        self._stopRun = False
        self._is_running = False
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', self.port))

    def stop(self):
        self.log.debug('Transmitter stop() called')
        _stopRun = True
    
    def run(self):
        _is_running = True
        self.log.debug('Transmitter thread started')
        self._stopRun = False
        while not self._stopRun:
            try:
                data, addr = self.sock.recvfrom(1500)
                # print (addr)
                p = Packet(data)
                if p is not None:
                    send(p)
            except Exception as e:
                self.log.exception(f'Error in Transmitter thread {str(e)}')
        self.log.debug('Transmitter thread stoped')


if __name__ =='__main__':
    t = Transmitter('USB Gigabit Ethernet', "dst='192.168.4.*'")
    t.start()
    sleep(30)
    t.stop()
    while r.is_running():
        sleep(0.1)
        print ('.')
