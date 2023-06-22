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
    Make sure you have Python 3.x and pip installed.

## Usage

- **Tool 1: ARP Spoofer** - Spoofs a target computer and gateway to man-in-the-middle both

    python3 arp_spoofer.py -t (insert target machine IP) -g (insert gateway IP)

- **Tool 2: MAC Changer** - Changes the MAC address of your machine

    python3 mac_changer.py -i (insert interface to change; e.g. 'eth0') -m (insert new MAC address)

- **Tool 3: Network Scanner** - Scans an IP or range of IPs for active connections

    python3 network_scanner.py -t (insert target or range to scan' e.g. 10.0.2.1, 10.0.2.1/24, etc.)

- **Tool 4: Packet Sniffer** - Sniffs all packets running through an interface. Specifically searches HTTP requests for URLs and Username/Passwords. Will likely want to run in conjuction with ARP spoofer so that target traffic is flowing through your interface.

    python3 packet_sniffer.py -i (insert insterface to sniff; e.g. 'eth0')

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
