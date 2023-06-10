import scapy.all as scapy
import argparse


def main():
    target = get_arguments()
    check_args(target)
    #perform a scan of clients on the specified network
    found_connections = scan(target)

    #print results returned from scan
    print('ip\t\t\tmac Address\n---------------------------------------------------')
    for client in found_connections:
        print(f'{client["ip"]}\t\t{client["mac"]}')


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help="ip that user wishes to scan.")
    options = parser.parse_args()

    return options.target


def check_args(target):
    if target == None:
        print('Please input a target to scan using the "-t" command.\n(Use --help for help)')
        exit()


def scan(ip):
    #creates an arp request packet at target ip
    arp_request = scapy.ARP(pdst=ip)
    #creates a broadcast packet to the generic broadcast mac addr
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    #combines the arp and broadcast packets for later use
    arp_request_broadcast = broadcast/arp_request
    #sends arp packet via srp and stores answered and unanswered packet responses
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    #creates a list to return values
    found_connections = []

    #appends our found_connections list with dicts of parsed ip/mac info
    for element in answered_list:
        clientDict = {
            'ip': element[1].psrc,
            'mac': element[1].hwsrc
            }
        found_connections.append(clientDict)
    
    return found_connections


if __name__ == "__main__":
    main()