#!/usr/bin/env python
import scapy.all as scapy
import argparse
import time


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
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            if real_mac != response_mac:
                print('[+] This network is being ARP spoofed.')
        except IndexError:
            pass


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
    parser.add_argument('-i', '--interface', dest='interface', help="Defines which interface you want to sniff (most commonly eth0).")
    options = parser.parse_args()

    return options.interface


def check_args(interface):
    if interface == None:
        print('Please input an interface to sniff using the "-i" command.\n(Use --help for help)')
        exit()


if __name__ == '__main__':
    main()