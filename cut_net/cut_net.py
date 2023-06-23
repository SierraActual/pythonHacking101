#!/usr/bin/env python
import netfilterqueue
import pyptables

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
    #currently drops packets
    packet.drop()
    #to print and accept packets:
    '''
    print(packet)
    packet.accept()
    '''

    #TODO use argparse to define if you want to drop or accept


if __name__ == '__main__':
    main()