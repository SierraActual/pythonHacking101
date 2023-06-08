import scapy.all as scapy


def main():
    scan("209.151.148.1")


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    print(arp_request.summary())


if __name__ == "__main__":
    main()