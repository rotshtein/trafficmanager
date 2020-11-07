import threading
from scapy.all import *
from time import sleep
import socket
from Receiver import Receiver
from Trasmitter import Transmitter

class TrafficManager(threading.Thread):
    def __init__(self, iface='eth1', filter="dst='192.168.137.0'", rx_port=50000, tx_port = 50001):
        super().__init__()
        self.log = logging.getLogger(self.__class__.__name__)
        self.iface = iface
        self.filter = filter
        self.rx_port = rx_port
        self.tx_port = tx_port
        self._stopRun = False
        self._is_running = False
        self.transmitter = None
        self.receiver = None

    def start(self):
        self._is_running = True
        self.create_receiver()
        self.create_transmiter()

    def stop(self):
        _stopRun = True
        if self.transmitter is not None:
            self.transmitter.stop()
            self.transmitter = None
        if self.receiver is not None:
            self.receiver.stop()
            self.receiver = None
        self._is_running = False
    
    def create_receiver(self):
        self.receiver = Receiver(self.iface, self.filter, self.rx_port)
        self.receiver.start()
    
    def create_transmiter(self):
        self.transmitter = Transmitter(self.iface, self.filter, self.tx_port)
        self.transmitter.start()
    