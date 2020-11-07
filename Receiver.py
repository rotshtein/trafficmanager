import threading
from scapy.all import *
from time import sleep
import socket
import logging

class Receiver(threading.Thread):
    def __init__(self, iface, filter, port=50000):
        super().__init__()
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug(f'Receiver started: iface={iface}, filter={filter}, port={port}')
        self.iface = iface
        self.filter = filter
        self._stopRun = False
        self._is_running = False
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    def stop(self):
        self.log.debug('Receiver stop() called')
        self._stopRun = True
        #close(self.sock)

    def is_running(self):
        return self._is_running

    def run(self):
        self._is_running = True
        self.log.debug('Receiver thread started')
        while not self._stopRun:
            try:
                sniff(iface=self.iface, filter=self.filter, prn=self.pkt_callback, store=0, timeout=1)
            except Exception as e:
                self.log.exception(f'Error in Receiver thread {str(e)}')
        self.log.debug('Receiver thread stoped')
        self._is_running = False


    def pkt_callback(self, pkt):
        # pkt.show() # debug statement
        try:
            ip = pkt.getlayer(IP)
            if ip is None:
                return
            buffer = bytes(ip)
            try:
                self.sock.sendto(buffer,('127.0.0.1', self.port))
            except Exception as ex:
                self.log.exception(f'Error in Receiver / sendto 127.0.0.1 {str(ex)}')
        except Exception as e:
            self.log.exception(f'Error in Receiver / pkt_callback {str(e)}')
        


if __name__ =='__main__':
    r = Receiver('USB Gigabit Ethernet', "dst='192.168.4.*'")
    r.start()
    sleep(30)
    r.stop()
    while r.is_running():
        sleep(0.1)
        print ('.')

