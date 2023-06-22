#!/usr/bin/env python
import netfilterqueue

def main():
    #Need to create network que using iptables command:
        #iptables -I FORWARD -j NFQUEUE --queue-num 0
    #Upon completion execute flush command:
        #iptables --flush
    #TODO automate above.
    
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()


def process_packet(packet):
    packet.drop()


if __name__ == '__main__':
    main()