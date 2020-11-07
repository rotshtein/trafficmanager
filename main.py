from TrafficManager import TrafficManager
from time import sleep
import argparse
from sys import argv, exit
import os
import logging
from logging.handlers import RotatingFileHandler

def init_log(level=logging.DEBUG):
    # FORMATTER = logging.Formatter('%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s')
    FORMATTER = logging.Formatter('%(asctime)s — %(name)s — %(levelname)s:\t%(message)s')
    LOG_FILE = 'TrafficManager.log'
    logging.basicConfig(level=logging.DEBUG, datefmt='%m-%d %H:%M')
    logger = logging.getLogger()
    logger.removeHandler(logger.handlers[0])

    handler = RotatingFileHandler(LOG_FILE, mode='a', maxBytes=1000000, backupCount=10, encoding='utf-8', delay=0)
    handler.setLevel(level)
    handler.setFormatter(FORMATTER)
    logging.getLogger('').addHandler(handler)

def main():
    init_log(level=logging.DEBUG)
    log = logging.getLogger('main')
    log.info("Traffic Manager starts")
    parser = argparse.ArgumentParser(description='RCC Traffic Manager')
    parser.add_argument('-r', '--rx_port', type=int, action='store', default=50000, help='rx port for the communication with the RCC')
    parser.add_argument('-t', '--tx_port', type=int, action='store', default=50001, help='tx port for the communication with the RCC')
    parser.add_argument('-f', '--filter', type=str, action='store', default="dst='192.168.137.*'", help='Filetr. Set the remote network filter')
    parser.add_argument('-i', '--iface', type=str, action='store', default="eth1", help='The locaal interface to use')
    parser.add_argument('-l', '--list', action='store_true', help='Show interface list')

    args = parser.parse_args(argv[1:])  # ('-r 50000 -t 50001 -f dst="192.168.4.*" -i USB' ).split())

    if args.list == True:
        from scapy.all import get_if_list, get_windows_if_list
        if os.name == 'nt':
            list = get_windows_if_list()
            for iface in list:
                print (f'{iface["description"]} \t\t {iface["ips"]}')
        else:
            list = get_if_list()
            for iface in list:
                print (iface)
        exit(0)        

    tm = TrafficManager(iface=args.iface, filter=args.filter, rx_port=args.rx_port, tx_port=args.tx_port)
    tm.start()
    log.info("Traffic Manager active")

    while(True):
        sleep(10)
    log.info("Traffic Manager exit")


if __name__ == '__main__':
    main()