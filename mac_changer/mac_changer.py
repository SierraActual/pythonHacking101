#!/usr/bin/env python

import subprocess
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help="Interface that user wishes to change.")
    parser.add_option('-m', '--mac', dest='new_mac', help="Mac address that user wishes to change to.")
    (options, arguments) = parser.parse_args()

    return options.interface, options.new_mac


def check_args(interface, new_mac):
    if interface == None:
        print('Please input an interface to change using the "-i" command.\n(Use mac_changer --help for help)')
        exit()
    if new_mac == None:
        print('Please input a MAC address to change to using the "-m" command.\n(Use mac_changer --help for help)')
        exit()


def mac_change(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}.")
    #subprocess.run('ifconfig', interface, 'down')
    #subprocess.run('ifconfig', interface, 'hw', 'ether', new_mac)
    #subprocess.run('ifconfig', interface, 'up')


def main():
    interface, new_mac = get_arguments()
    check_args(interface, new_mac)
    mac_change(interface, new_mac)


if __name__ == '__main__':
    main()