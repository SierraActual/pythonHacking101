import scapy.all as scapy

# ARP scan for all specified IPs
def scan(ip):
    scapy.arping(ip)

# Performs scan on IP in quotes
scan("(ip)/24")