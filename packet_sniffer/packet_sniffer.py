#!/usr/bin/env python
import scapy.all as scapy
import argparse
import time
from scapy.layers import http


def main():
    #get user arguments
    interface = get_arguments()
    check_args(interface)

    try:
        sniff(interface)
    except KeyboardInterrupt:
        print('[+] Halting sniff process. Exiting...')


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        print(packet)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface', dest='interface', help="Defines which interface you want to sniff (most commonly eth0).")
    options = parser.parse_args()

    return options.interface


def check_args(interface):
    if interface == None:
        print('Please input an interface to sniff using the "-i" command.\n(Use --help for help)')
        exit()


if __name__ == '__main__':
    main()