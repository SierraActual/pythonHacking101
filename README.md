# Python Hacking Tools

A collection of Python-based hacking tools for various security testing and penetration testing tasks.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository:**

    git clone https://github.com/SierraActual/pythonHacking101.git


2. **Navigate to the project directory:**

    cd pythonHacking101


3. **Install the required dependencies using pip:**

    pip3 install -r requirements.txt
    (Make sure you have Python 3.x and pip installed)

4. **Install needed system-level dependencies:**

    apt-get update && apt-get install -y libnfnetlink-dev && apt-get install -y libnetfilter-queue-dev
   
    (may need to run as root)

## Usage

- **Tool 1: ARP Spoofer** - Spoofs a target computer and gateway to man-in-the-middle both

    python3 arp_spoofer/arp_spoofer.py -t (insert target machine IP) -g (insert gateway IP)

- **Tool 2: MAC Changer** - Changes the MAC address of your machine

    python3 mac_changer/mac_changer.py -i (insert interface to change; e.g. 'eth0') -m (insert new MAC address)

- **Tool 3: Network Scanner** - Scans an IP or range of IPs for active connections

    python3 network_scanner/network_scanner.py -t (insert target or range to scan' e.g. 10.0.2.1, 10.0.2.1/24, etc.)

- **Tool 4: Packet Sniffer** - Sniffs all packets running through an interface. Specifically searches HTTP requests for URLs and Username/Passwords. Will likely want to run in conjuction with ARP spoofer so that target traffic is flowing through your interface.

    python3 packet_sniffer/packet_sniffer.py -i (insert insterface to sniff; e.g. 'eth0')

- **Tool 5: Network cut** - Adds network packets to a queue to potentially modify. Currently drops all packets, but options in code to forward them.

    **WARNING: Automated iptables modification not functioning. Will need to modify iptables based on use-case.**
        **(e.g. iptables -I FORWARD -j NFQUEUE --queue-num 0)**
        **When complete ensure you flush with "iptables --flush"**
        **Above may also have issues on newer systems as iptables is depreciated. Will adjust for newer solution at a later date**

    python3 cut_net/cut_net.py

- **Tool 6: DNS Spoofer** - Used to man-in-the-middle DNS requests already running through your machine (likely by using ARP spoofer). Redirects DNS requests to chosen IPs.

    **WARNING: Automated iptables modification not functioning. Will need to modify iptables based on use-case.**
        **(e.g. iptables -I FORWARD -j NFQUEUE --queue-num 0)**
        **When complete ensure you flush with "iptables --flush"**
        **Above may also have issues on newer systems as iptables is depreciated. Will adjust for newer solution at a later date**


    python3 dns_spoofer/dns_spoofer.py

- **Tool 7: Download Replacer** - Used to man-in-the-middle download requests already running through your machine (likely by using ARP spoofer). Redirects downloads to chosen file links.

    **WARNING: Automated iptables modification not functioning. Will need to modify iptables based on use-case.**
        **(e.g. iptables -I FORWARD -j NFQUEUE --queue-num 0)**
        **When complete ensure you flush with "iptables --flush"**
        **Above may also have issues on newer systems as iptables is depreciated. Will adjust for newer solution at a later date**


    **WARNING: Need to enable IP forwarding with "echo 1 > /proc/sys/net/ipv4/ip_forward" or file flows through middle machine will not be enabled.**

    python3 replace_downloads/replace_downloads.py

- **Tool 8: Code Injector** - Used to man-in-the-middle HTTP requests and responses (likely by using ARP spoofer) and inject custom code into websites.

    **WARNING: Automated iptables modification not functioning. Will need to modify iptables based on use-case.**
        **(e.g. iptables -I FORWARD -j NFQUEUE --queue-num 0)**
        **When complete ensure you flush with "iptables --flush"**
        **Above may also have issues on newer systems as iptables is depreciated. Will adjust for newer solution at a later date**


    python3 code_injector/code_injector.py

- **Tool 9: ARP Spoof Detector** - Runs scans on ARP pings to see if anyone is attempting to ARP spoof your computer.

    python3 arpspoof_detector/arpspoof_detector.py

- **Tool 10: WiFi Passowr Stealer** - Runs windows commands to steal all WiFi passwords stored on the system. It then emails them to your email. 
    **WARNING** You need to use gmail, or edit the smtp server info in the send_mail function. You also need to put your email, and generated app password in the two variables at the top.

    python3 malware/wifi_password/wifi_password_stealer.py

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch: git checkout -b my-feature.
3. Make your changes and commit them: git commit -m 'Add new feature'.
4. Push to the branch: git push origin my-feature.
5. Submit a pull request.

For bug reports, feature requests, or any other questions, please open an issue on the repository.

## License
This project is licensed under the MIT License.
Feel free to modify and customize the content as per your requirements.
