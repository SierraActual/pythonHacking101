import scapy.all as scapy


def main():
    scan("209.151.148.1")


def scan(ip):
    #creates an arp request packet at target ip
    arp_request = scapy.ARP(pdst=ip)
    #creates a broadcast packet to the generic broadcast mac addr
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    #combines the arp and broadcast packets for later use
    arp_request_broadcast = broadcast/arp_request

    #sends arp packet via srp and stores answered and unanswered packet responses
    answered_list = scapy.srp(arp_request_broadcast, timeout=1)[0]
    
    for element in answered_list:
        print(element[1].psrc)
        print(element[1].hwsrc)
        print('---------------------------------------------------')


if __name__ == "__main__":
    main()